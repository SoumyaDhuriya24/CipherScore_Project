import sys
import os

# --- PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_dir, 'differential_cryptanalysis_lib')
if lib_path not in sys.path:
    sys.path.append(lib_path)

# Try importing the attack library safely
from core.attacks import StatisticalTester, LinearTester, DifferentialTester, TimingTester, AlgebraicTester, SimulatedAttacks

# Legacy import removal since we replaced it
analize_cipher = None

from core.metrics import calculate_avalanche_effect, measure_performance

class CipherAuditAgent:
    # ---------------------------------------------------------
    # ERROR WAS HERE: We must accept 'cipher_instance' in __init__
    # ---------------------------------------------------------
    def __init__(self, cipher_instance):
        self.cipher = cipher_instance
        self.results = {}

    def run_full_audit(self, rounds=1000):
        cipher_name = getattr(self.cipher, 'name', 'Custom Cipher')
        print(f"🕵️ Agent: Starting audit for {cipher_name}...")
        
        # 1. Security Metrics (Avalanche)
        # using a dummy key for testing metrics
        dummy_key = b'0123456789abcdef' 
        
        try:
            av_score = calculate_avalanche_effect(self.cipher, dummy_key, rounds=500) # Reduced rounds for speed
            self.results['Avalanche Score'] = f"{av_score:.2f}%"
        except Exception as e:
            self.results['Avalanche Score'] = "0.00% (Error)"
            print(f"Avalanche Error: {e}")

        # 2. Performance Test
        try:
            dummy_data = b'Hello World Data'
            speed, mem = measure_performance(self.cipher, dummy_data, dummy_key)
            self.results['Encryption Speed (ms)'] = f"{speed:.4f} ms"
            self.results['Peak Memory (KB)'] = f"{mem:.2f} KB"
        except:
             self.results['Encryption Speed (ms)'] = "N/A"

        # 3. Comprehensive Attack Suite
        # Generate a large sample of ciphertext for statistical testing
        sample_data = b""
        try:
            for _ in range(200): # 16 * 200 = 3200 bytes
                 p = os.urandom(16)
                 c = self.cipher.encrypt(p, dummy_key)
                 if isinstance(c, bytes): sample_data += c
                 else: sample_data += str(c).encode() 
        except:
            sample_data = b"\x00" * 100 # Fallback

        # Check randomness
        entropy = StatisticalTester.calculate_entropy(sample_data)
        
        # Run Tests
        tests = []
        tests.append(StatisticalTester.monobit_test(sample_data))
        tests.append(StatisticalTester.runs_test(sample_data))
        tests.append(StatisticalTester.chisquare_test(sample_data))
        tests.append(LinearTester.linear_bias_check(self.cipher))
        tests.append(DifferentialTester.run_differential_test(self.cipher))
        
        # New Phase 2 Attacks
        tests.append(TimingTester.run_timing_test(self.cipher))
        tests.append(AlgebraicTester.check_key_strength(len(dummy_key)))
        
        # Educational Simulations
        power_sim = SimulatedAttacks.generate_power_trace()
        self.results['power_trace'] = power_sim['trace_data'] # Separate field for UI chart
        
        # Compile Weaknesses
        weaknesses = []
        for t in tests:
            if not t['passed']:
                weaknesses.append(f"{t['name']} FAILED: {t['details']}")

        # Populate Results
        self.results['weaknesses'] = weaknesses
        self.results['randomness_stats'] = {
            "entropy": entropy,
            "chi_square_p_value": tests[2]['score'] # Passing raw score as p-value mock for UI
        }
        
        # Final Score Calculation
        score = 100
        if len(weaknesses) > 0: score -= 20 * len(weaknesses)
        if entropy < 7.5: score -= 15
        if float(av_score) < 45 or float(av_score) > 55: score -= 20
        
        self.results['final_score'] = max(0, score)

        return self.results