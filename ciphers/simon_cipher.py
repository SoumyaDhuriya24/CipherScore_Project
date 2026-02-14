from core.interfaces import BaseCipher
# Import from your LOCAL file now
from ciphers.simon_speck_logic import SimonCipherEngine

class SimonCipher(BaseCipher):
    @property
    def name(self):
        return "Simon-64/128 (NSA Lightweight)"

    def encrypt(self, plaintext, key):
        # 1. Setup Engine
        # Truncate/Pad key to 16 bytes
        clean_key = key.ljust(16, b'\0')[:16]
        engine = SimonCipherEngine(clean_key)
        
        # 2. Prepare Input (8 bytes for 64-bit block)
        pt_padded = plaintext.ljust(8, b'\0')[:8]
        pt_int = int.from_bytes(pt_padded, 'big')
        
        # 3. Encrypt
        ct_int = engine.encrypt(pt_int)
        
        return ct_int.to_bytes(8, 'big')

    def decrypt(self, ciphertext, key):
        return ciphertext # Not needed for Avalanche test