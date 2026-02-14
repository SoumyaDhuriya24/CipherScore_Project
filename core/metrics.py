# core/metrics.py
import time
import tracemalloc

def calculate_avalanche_effect(cipher, key, rounds=1000):
    """
    Runs bit-flip tests to see if output changes by ~50%.
    """
    import random
    
    total_diff_ratio = 0
    
    for _ in range(rounds):
        # 1. Generate random input (8 bytes / 64 bits)
        p1 = random.randbytes(8)
        
        # 2. Flip 1 bit
        # (Logic to flip a random bit in p1 to create p2)
        bit_idx = random.randint(0, 63)
        p1_int = int.from_bytes(p1, 'big')
        p2_int = p1_int ^ (1 << bit_idx)
        p2 = p2_int.to_bytes(8, 'big')
        
        # 3. Encrypt both
        c1 = cipher.encrypt(p1, key)
        c2 = cipher.encrypt(p2, key)
        
        # 4. Count diff (Hamming distance)
        diff = bin(int.from_bytes(c1, 'big') ^ int.from_bytes(c2, 'big')).count('1')
        total_diff_ratio += (diff / (len(c1) * 8))

    return (total_diff_ratio / rounds) * 100

def measure_performance(cipher, plaintext, key, iterations=10000):
    """
    Measures Speed (Time) and Memory (RAM).
    """
    # Measure Memory
    tracemalloc.start()
    
    # Measure Time
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        cipher.encrypt(plaintext, key)
        
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    avg_time_ms = ((end_time - start_time) / iterations) * 1000
    peak_memory_kb = peak / 1024
    
    return avg_time_ms, peak_memory_kb