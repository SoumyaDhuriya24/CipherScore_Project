import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import CipherAuditAgent
from core.loader import load_custom_cipher_from_text # <--- NEW IMPORT
from ciphers.test_cipher import SimpleXORCipher 
from ciphers.ascon_cipher import AsconCipher
from ciphers.simon_cipher import SimonCipher
from ciphers.speck_cipher import SpeckCipher
from ciphers.present_cipher import PresentCipher

st.set_page_config(page_title="CipherScore: Security Evaluator", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ CipherScore: Lightweight Cipher Evaluator")
st.markdown("---")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuration")

cipher_option = st.sidebar.selectbox(
    "Select Algorithm",
    (
        "Simple XOR (Test)", 
        "Ascon-128 (NIST Standard)",
        "Simon-64/128 (NSA Lightweight)",
        "Speck-64/128 (Software Optimized)",
        "PRESENT-80 (ISO Standard)",
        "✨ Custom (Paste Code)"  # <--- NEW OPTION
    )
)

rounds = st.sidebar.slider("Test Rounds (Avalanche)", 100, 5000, 1000)

# --- MAIN LOGIC ---
target_cipher = None

# If user selects "Custom", we show the editor instead of running immediately
if cipher_option == "✨ Custom (Paste Code)":
    st.info("Paste your Python cipher class below. It must have `.encrypt(plaintext, key)` method.")
    
    # Default Template Code
    default_code = """class MyCustomCipher:
    @property
    def name(self):
        return "My Experimental Cipher"

    def encrypt(self, plaintext, key):
        # Example: Simple shift (Caesar) - REPLACE THIS
        # Ensure inputs are ints or bytes
        if isinstance(plaintext, bytes):
            pt_int = int.from_bytes(plaintext, 'big')
            key_int = int.from_bytes(key[:8], 'big')
        else:
            pt_int = plaintext
            key_int = key
            
        # Your Logic Here
        result = pt_int ^ key_int
        return result.to_bytes(8, 'big')

    def decrypt(self, ciphertext, key):
        return ciphertext # Logic here
"""
    
    # Text Editor
    code_input = st.text_area("Python Code Editor", value=default_code, height=300)
    
    # CORRECT (Only one string)
    if st.button("⚡ Compile & Run Audit"):
        try:
            # Load the user's code dynamically
            target_cipher = load_custom_cipher_from_text(code_input)
            st.success(f"Successfully loaded: {target_cipher.name}")
        except Exception as e:
            st.error(f"Compilation Failed: {e}")
            st.stop()

else:
    # Standard Selection Logic
    if st.sidebar.button("🚀 Run Full Audit"):
        if cipher_option == "Simple XOR (Test)": target_cipher = SimpleXORCipher()
        elif cipher_option == "Ascon-128 (NIST Standard)": target_cipher = AsconCipher()
        elif cipher_option == "Simon-64/128 (NSA Lightweight)": target_cipher = SimonCipher()
        elif cipher_option == "Speck-64/128 (Software Optimized)": target_cipher = SpeckCipher()
        elif cipher_option == "PRESENT-80 (ISO Standard)": target_cipher = PresentCipher()

# --- RUN AUDIT (Common for both Custom and Standard) ---
if target_cipher:
    agent = CipherAuditAgent(target_cipher)
    
    with st.spinner(f"🕵️ Auditing {target_cipher.name}... Running {rounds} rounds..."):
        report = agent.run_full_audit(rounds=rounds)
        
    # --- RESULTS DISPLAY ---
    # ROW 1: Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    avalanche = report.get('Avalanche Score', '0%')
    speed = report.get('Encryption Speed (ms)', '0 ms')
    memory = report.get('Peak Memory (KB)', '0 KB')
    attack_status = report.get('Attack Status', 'Not Run')

    col1.metric("Avalanche Effect", avalanche, "Target: 50%")
    col2.metric("Encryption Speed", speed, "Lower is Better")
    col3.metric("Peak Memory", memory, "For IoT < 10KB")
    col4.metric("Attack Resistance", attack_status, "Simulation Result")
    
    st.markdown("---")

    # ROW 2: Visualization
    viz_col, data_col = st.columns([2, 1])
    with viz_col:
        try:
            av_val = float(str(avalanche).replace('%', '').strip())
        except:
            av_val = 0.0
        
        chart_data = pd.DataFrame({
            'Metric': ['Avalanche Score', 'Ideal Target'],
            'Percentage': [av_val, 50.0]
        })
        
        fig, ax = plt.subplots(figsize=(6, 3))
        colors = ['red' if abs(av_val - 50) > 5 else 'green', 'gray']
        ax.bar(chart_data['Metric'], chart_data['Percentage'], color=colors)
        ax.set_ylim(0, 100)
        ax.axhline(50, color='black', linestyle='--', alpha=0.5)
        st.pyplot(fig)

    with data_col:
        st.json(report)