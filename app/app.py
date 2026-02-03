import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import CipherAuditAgent
from core.loader import load_custom_cipher_from_text
from ciphers.test_cipher import SimpleXORCipher 
from ciphers.ascon_cipher import AsconCipher
from ciphers.simon_cipher import SimonCipher
from ciphers.speck_cipher import SpeckCipher
from ciphers.present_cipher import PresentCipher

st.set_page_config(page_title="CipherScore: Universal Validator", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .metric-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; }
    .pass { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; }
    .fail { color: #721c24; background-color: #f8d7da; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ CipherScore: Universal Validator")
st.markdown("---")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.radio("Select Mode", ["📚 Standard Library", "✨ Custom Lab (Paste Code)"])
rounds = st.sidebar.slider("Avalanche Test Rounds", 100, 5000, 1000)

target_cipher = None

# ==========================================
# MODE 1: STANDARD LIBRARY (Pre-built)
# ==========================================
if mode == "📚 Standard Library":
    algo = st.sidebar.selectbox("Algorithm", 
        ("Ascon-128 (NIST)", "Simon-64/128 (NSA)", "Speck-64/128", "PRESENT-80", "Simple XOR (Weak)"))
    
    if st.sidebar.button("🚀 Run Analysis"):
        if "Ascon" in algo: target_cipher = AsconCipher()
        elif "Simon" in algo: target_cipher = SimonCipher()
        elif "Speck" in algo: target_cipher = SpeckCipher()
        elif "PRESENT" in algo: target_cipher = PresentCipher()
        elif "XOR" in algo: target_cipher = SimpleXORCipher()

# ==========================================
# MODE 2: CUSTOM LAB (Universal Code Runner)
# ==========================================
elif mode == "✨ Custom Lab (Paste Code)":
    st.info("Paste your cipher code below. Requirements: Class must have `.encrypt(plaintext, key)` method.")

    # TEMPLATES
    template_options = {
        "Empty Skeleton": """class MyCipher:
    def encrypt(self, plaintext, key):
        # Your logic here
        return plaintext
    def decrypt(self, ciphertext, key):
        return ciphertext""",
        
        "Robust AES-GCM (Best Practice)": """import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CustomAES:
    @property
    def name(self): return "AES-GCM (Custom)"
    
    # NOTE: No __init__ arguments! We use the key passed to encrypt()
    def encrypt(self, plaintext, key):
        # Clean Inputs
        data = plaintext if isinstance(plaintext, bytes) else str(plaintext).encode()
        # Force Key to 32 bytes
        k = key.ljust(32, b'\\0')[:32] if isinstance(key, bytes) else str(key).encode().ljust(32, b'\\0')[:32]
        
        # Encrypt
        aes = AESGCM(k)
        nonce = os.urandom(12)
        return nonce + aes.encrypt(nonce, data, None)

    def decrypt(self, ciphertext, key):
        return ciphertext # Logic omitted for audit""",
        
        "Weak XOR (For Failure Demo)": """class WeakXOR:
    @property
    def name(self): return "Weak XOR Cipher"
    
    def encrypt(self, plaintext, key):
        # Simple XOR (Insecure)
        pt = int.from_bytes(plaintext, 'big') if isinstance(plaintext, bytes) else plaintext
        k = int.from_bytes(key[:8], 'big') if isinstance(key, bytes) else key
        return (pt ^ k).to_bytes(8, 'big')

    def decrypt(self, ct, key): return ct"""
    }
    
    selected_template = st.selectbox("Load Template:", list(template_options.keys()))
    code_input = st.text_area("Code Editor", value=template_options[selected_template], height=350)

    # MANUAL TEST SECTION
    st.subheader("🧪 Step 1: Manual Verification")
    c1, c2, c3 = st.columns([2, 1, 1])
    test_msg = c1.text_input("Test Message", "SecretData")
    test_key = c2.text_input("Test Key", "MyKey123")
    
    if c3.button("Verify Code"):
        try:
            # 1. Try to Load
            temp_cipher = load_custom_cipher_from_text(code_input)
            
            # 2. Try to Encrypt
            res = temp_cipher.encrypt(test_msg.encode(), test_key.encode())
            
            # 3. Success!
            st.success("✅ Code is Valid! Output generated:")
            st.code(res.hex().upper() if isinstance(res, bytes) else str(res))
            st.session_state['valid_code'] = True
            
        except Exception as e:
            st.error(f"{e}")
            st.session_state['valid_code'] = False

    st.markdown("---")
    
    # RUN AUDIT BUTTON
    if st.button("🚀 Run Full Security Audit"):
        # We try to run it even if they didn't verify, but we wrap it safely
        try:
            target_cipher = load_custom_cipher_from_text(code_input)
        except Exception as e:
            st.error(f"Cannot Start Audit: {e}")

# ==========================================
# REPORT GENERATION (Common for both modes)
# ==========================================
if target_cipher:
    try:
        agent = CipherAuditAgent(target_cipher)
        
        with st.spinner(f"Running 4-Stage Security Audit on {getattr(target_cipher, 'name', 'Custom Cipher')}..."):
            report = agent.run_full_audit(rounds=rounds)

        # PARSE RESULTS
        av = float(str(report.get('Avalanche Score', '0')).strip('%'))
        speed_str = str(report.get('Encryption Speed (ms)', '0'))
        speed = float(speed_str.replace('ms', '').strip())
        status = report.get('Attack Status', 'Unknown')

        # DASHBOARD
        st.success(f"Audit Complete: {getattr(target_cipher, 'name', 'Custom Cipher')}")
        
        # 1. METRICS
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Avalanche Effect", f"{av}%", "Target: 50%")
        m2.metric("Speed", f"{speed} ms", "Lower is better")
        m3.metric("Memory", report.get('Peak Memory (KB)', '0 KB'))
        m4.metric("Attack Status", "SAFE" if "SAFE" in status else "FAIL", status)

        st.markdown("---")

        # 2. FINAL VERDICT ENGINE
        st.subheader("🏁 IoT Suitability Verdict")
        
        is_secure = (40 <= av <= 60) and ("SAFE" in status)
        is_light = (speed < 15.0)
        
        if is_secure and is_light:
            st.markdown(f'<div class="pass"><h3>✅ APPROVED FOR IOT</h3><p>This algorithm is both secure (Avalanche {av}%) and lightweight.</p></div>', unsafe_allow_html=True)
        elif not is_secure:
            st.markdown(f'<div class="fail"><h3>❌ REJECTED (INSECURE)</h3><p>Failed security checks. Do not use for sensitive data.</p></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Usable, but performance is suboptimal for low-power devices.")

        # 3. VISUALS
        v_col, d_col = st.columns([2, 1])
        with v_col:
            st.caption("Avalanche Distribution")
            df = pd.DataFrame({'Metric': ['Your Code', 'Ideal'], 'Score': [av, 50]})
            st.bar_chart(df.set_index('Metric'))
            
        with d_col:
            st.json(report)
            
    except Exception as e:
        st.error(f"Runtime Error during Audit: {e}")
        st.info("Check your code logic. Did you return bytes? Did you handle integers correctly?")