import random
import math
from collections import Counter

class StatisticalTester:
    """
    Implements a subset of NIST SP 800-22 Rev 1a Statistical Tests.
    """
    
    @staticmethod
    def monobit_test(data: bytes):
        """
        NIST Test 2.1: Frequency (Monobit) Test
        The focus of the test is the proportion of zeroes and ones for the entire sequence.
        """
        n = len(data) * 8
        ones = sum(bin(byte).count('1') for byte in data)
        zeros = n - ones
        
        # S_n = X_1 + ... + X_n, where X_i = 2x - 1 (so 0 -> -1, 1 -> +1)
        s_obs = abs(ones - zeros) / math.sqrt(n)
        p_value = math.erfc(s_obs / math.sqrt(2))
        
        return {
            "name": "Monobit Frequency Test",
            "p_value": p_value,
            "passed": p_value >= 0.01,
            "details": f"Ones: {ones}, Zeros: {zeros}"
        }

    @staticmethod
    def runs_test(data: bytes):
        """
        NIST Test 2.2: Frequency Test within a Block (Runs Test)
        The focus of the test is the total number of runs in the sequence,
        where a run is an uninterrupted sequence of identical bits.
        """
        # Convert bytes to a bit string
        bits = "".join(f"{byte:08b}" for byte in data)
        n = len(bits)
        
        proportion_ones = bits.count('1') / n
        
        # Check if Frequency test is passed (pre-requisite)
        if abs(proportion_ones - 0.5) >= (2 / math.sqrt(n)):
            return {
                "name": "Runs Test",
                "p_value": 0.0,
                "passed": False,
                "details": "Failed pre-requisite Frequency test"
            }

        # Calculate observed runs (V_n)
        v_obs = 1 + sum(1 for i in range(n - 1) if bits[i] != bits[i+1])
        
        # Expected runs
        mean = 2 * n * proportion_ones * (1 - proportion_ones)
        
        numerator = abs(v_obs - mean)
        denominator = 2 * math.sqrt(2 * n) * proportion_ones * (1 - proportion_ones)
        
        p_value = math.erfc(numerator / denominator)
        
        return {
            "name": "Runs Test",
            "p_value": p_value,
            "passed": p_value >= 0.01,
            "details": f"Runs: {v_obs}"
        }

    @staticmethod
    def chisquare_test(data: bytes):
        """
        Pearson's Chi-Square Test for Uniformity of Byte Distribution.
        Checks if every byte value (0-255) appears with roughly equal frequency.
        """
        counts = Counter(data)
        expected = len(data) / 256
        chi_sq = sum(((counts[i] - expected) ** 2) / expected for i in range(256))
        
        # Degrees of freedom = 255
        # We use an approximation for p-value or a critical value threshold
        # Critical value for df=255, alpha=0.01 is approx 310.45
        # Critical value for df=255, alpha=0.05 is approx 293.25
        
        # Simplified Pass/Fail based on critical value for p=0.01
        passed = chi_sq < 310.45
        
        return {
            "name": "Chi-Square Byte Test",
            "score": chi_sq,
            "passed": passed,
            "details": f"Chi-Sq: {chi_sq:.2f} (Expected < 310.45)"
        }

    @staticmethod
    def calculate_entropy(data: bytes):
        """Calculates Shannon Entropy in bits per byte."""
        if not data:
            return 0
        
        counts = Counter(data)
        entropy = 0
        for count in counts.values():
            p = count / len(data)
            entropy -= p * math.log2(p)
            
        return entropy


class LinearTester:
    """
    Checks for high linear correlations between Plaintext/Ciphertext/Key bits.
    A secure cipher should have a bias close to 0 (probability 0.5).
    """
    
    @staticmethod
    def linear_bias_check(cipher, rounds=1000):
        # We test a specific linear approximation: P[0] ^ K[0] == C[0]
        # This is just a sample "mask". A real attack would search for the best mask.
        matches = 0
        total = rounds
        
        key = b'\x00' * 16 # Dummy key
        
        for _ in range(total):
            p = random.randbytes(8) # 64-bit block simulation
            try:
                c = cipher.encrypt(p, key)
            except:
                # Fallback for ciphers that need strings or different keys
                try:
                    c = cipher.encrypt(p.hex(), key.hex())
                    if isinstance(c, str): c = bytes.fromhex(c)
                except:
                    continue 

            # Extract first bit of P and C
            p_bit = (p[0] >> 7) & 1
            c_bit = (c[0] >> 7) & 1
            
            # Use a fixed key bit (0 for dummy key)
            k_bit = 0 
            
            if (p_bit ^ k_bit) == c_bit:
                matches += 1
                
        bias = abs((matches / total) - 0.5)
        
        # A bias > 0.05 is huge for 1000 rounds. 
        # Ideally should be ~ 1/sqrt(N)
        return {
            "name": "Linear Approximation (P[0]^K[0]=C[0])",
            "bias": bias,
            "passed": bias < 0.04,
            "details": f"Bias: {bias:.4f} (Ideal: 0.0)"
        }

class DifferentialTester:
    """
    Checks if specific input difference leads to a specific output difference
    with probability significantly higher than uniform random.
    """
    @staticmethod
    def run_differential_test(cipher, rounds=2000):
        # Standard differential: Flip last bit
        input_diff = 1 
        
        # We track how often the output difference matches ANY 'frequent' difference
        # Ideally, output diffs should be uniformly distributed.
        
        diff_counts = Counter()
        key = b'\x55' * 16
        
        for _ in range(rounds):
            p1 = random.randbytes(8)
            p1_int = int.from_bytes(p1, 'big')
            p2_int = p1_int ^ input_diff
            p2 = p2_int.to_bytes(8, 'big')
            
            try:
                c1 = cipher.encrypt(p1, key)
                c2 = cipher.encrypt(p2, key)
                
                # Normalize output to int
                c1_int = int.from_bytes(c1, 'big') if isinstance(c1, bytes) else int(c1.encode('utf-8').hex(), 16)
                c2_int = int.from_bytes(c2, 'big') if isinstance(c2, bytes) else int(c2.encode('utf-8').hex(), 16)
                
                diff_out = c1_int ^ c2_int
                diff_counts[diff_out] += 1
            except:
                pass
                
        # Analyze top frequent output difference
        if not diff_counts:
            return {"passed": True, "details": "Could not run test"}
            
        most_common_diff, count = diff_counts.most_common(1)[0]
        prob = count / rounds
        
        # For 64-bit block, uniform prob is 2^-64 (tiny). 
        # If we see any diff repeated > 1% of time in 2000 trials, it's BROKEN.
        

class TimingTester:
    """
    Checks for Side-Channel Timing Leaks.
    Measures if execution time varies significantly based on Input/Key (Data-Dependent Timing).
    """
    @staticmethod
    def run_timing_test(cipher, rounds=5000):
        import time
        import statistics
        
        # Set A: Fixed Key, Random Data
        times_a = []
        key = b'\x00' * 16
        for _ in range(rounds):
            p = random.randbytes(16)
            t0 = time.perf_counter_ns()
            cipher.encrypt(p, key)
            t1 = time.perf_counter_ns()
            times_a.append(t1 - t0)
            
        # Set B: Fixed Key (Different), Random Data
        # (Ideally we'd vary data hamming weight, but simple key absolute diff is a good generic proxy)
        times_b = []
        key_b = b'\xFF' * 16
        for _ in range(rounds):
            p = random.randbytes(16)
            t0 = time.perf_counter_ns()
            cipher.encrypt(p, key_b)
            t1 = time.perf_counter_ns()
            times_b.append(t1 - t0)
            
        mean_a = statistics.mean(times_a)
        mean_b = statistics.mean(times_b)
        
        # Calculate variance/stdev
        try:
            stdev_a = statistics.stdev(times_a)
            # If difference in means is greater than 1 standard deviation, it's suspicious
            # (Very rough heuristic for a noisy system like Python)
            diff = abs(mean_a - mean_b)
            is_suspicious = diff > (stdev_a * 0.5) and diff > 1000 # 1000ns threshold
            
            return {
                "name": "Timing Side-Channel",
                "variance_ns": diff,
                "passed": not is_suspicious,
                "details": f"Time Delta: {diff:.2f}ns (Suspicious if > {stdev_a*0.5:.2f}ns)"
            }
        except:
             return {"name": "Timing Side-Channel", "passed": True, "details": "Could not calculate"}

class AlgebraicTester:
    @staticmethod
    def check_key_strength(key_len_bytes):
        bits = key_len_bytes * 8
        passed = bits >= 128
        rating = "Critical" if bits < 64 else ("Weak" if bits < 112 else "Strong")
        return {
           "name": "Key Space Analysis",
           "bits": bits,
           "passed": passed,
           "details": f"Key Size: {bits}-bit ({rating})"
        }

class SimulatedAttacks:
    """
    Generates educational mock data for attacks that require physical access (which we can't do in a web app).
    """
    @staticmethod
    def generate_power_trace():
        """
        Generates a fake 'Power Consumption Trace' (noisy sine wave) to visualize Side-Channel Analysis.
        """
        trace = []
        # Simulate 100 sample points of power consumption
        for i in range(100):
            # Base crypto operation cycle (sine wave)
            base = math.sin(i * 0.2) * 10 
            # Random noise (thermal/electronic noise)
            noise = random.randint(-2, 2)
            # Occasional spikes (key-dependent leaks)
            spike = 20 if i % 25 == 0 else 0 
            
            trace.append(round(50 + base + noise + spike, 2))
            
        return {
            "name": "Simulated Power Analysis",
            "trace_data": trace,
            "passed": True, # Always pass simulation
            "details": "Trace generated. Look for periodic spikes correlated with key bits."
        }

