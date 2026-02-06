import sys
import os

# Ensure we can import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import CipherAuditAgent

class WeakXOR:
    @property
    def name(self): return "Weak XOR Cipher"
    
    def encrypt(self, plaintext, key):
        # Very weak encryption: Plaintext XOR Key
        # If lengths match, this is linear (P ^ K = C)
        # Monobit test should likely pass (random inputs -> random outputs)
        # But Linear test should FAIL mostly.
        
        if isinstance(plaintext, str): plaintext = plaintext.encode()
        if isinstance(key, str): key = key.encode()
        
        # Expand key to match plaintext length
        k_extended = (key * (len(plaintext) // len(key) + 1))[:len(plaintext)]
        
        ciphertext = bytes([p ^ k for p, k in zip(plaintext, k_extended)])
        return ciphertext

def test_attacks():
    print("Testing Attack Suite on WeakXOR...")
    cipher = WeakXOR()
    agent = CipherAuditAgent(cipher)
    
    # Run audit
    results = agent.run_full_audit(rounds=100)
    
    print("\n--- Results ---")
    print(f"Final Score: {results['final_score']}")
    print("Weaknesses Found:")
    for w in results['weaknesses']:
        print(f" - {w}")
        
    print("\nRandomness Stats:")
    print(results['randomness_stats'])

if __name__ == "__main__":
    test_attacks()
