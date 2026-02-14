# core/attacks.py
import random

def differential_attack_simulation(cipher, rounds=4):
    """
    Simulates a Differential Attack by checking if specific input differences
    lead to specific output differences with high probability.
    """
    print(f"⚔️ Attack Module: Launching Differential Attack on {cipher.name}...")
    
    # 1. Define a specific input difference (delta_P)
    # Example: 0000 0000 0000 0001
    delta_in = 0x0001 
    
    hits = 0
    trials = 5000
    
    for _ in range(trials):
        # Generate random plaintext P1
        p1 = random.randbytes(2) # Assuming 16-bit block for speed
        p1_int = int.from_bytes(p1, 'big')
        
        # Create P2 by XORing P1 with delta_in
        p2_int = p1_int ^ delta_in
        p2 = p2_int.to_bytes(2, 'big')
        
        # Encrypt both
        key = b'\x00'*10 # Dummy key
        c1 = cipher.encrypt(p1, key)
        c2 = cipher.encrypt(p2, key)
        
        # Check output difference
        diff_out = int.from_bytes(c1, 'big') ^ int.from_bytes(c2, 'big')
        
        # If output difference matches expected pattern (simplified)
        if diff_out == 0x0002: # Hypothetical expected diff
            hits += 1
            
    probability = hits / trials
    print(f"⚔️ Attack Result: Found differential path with Prob {probability:.4f}")
    
    # Return "Weak" if probability is significantly higher than random
    return "Weak" if probability > 0.05 else "Strong"