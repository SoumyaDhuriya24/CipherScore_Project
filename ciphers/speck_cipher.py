from core.interfaces import BaseCipher
# Import from your LOCAL file now
from ciphers.simon_speck_logic import SpeckCipherEngine

class SpeckCipher(BaseCipher):
    @property
    def name(self):
        return "Speck-64/128 (Software Optimized)"

    def encrypt(self, plaintext, key):
        clean_key = key.ljust(16, b'\0')[:16]
        engine = SpeckCipherEngine(clean_key)
        
        pt_padded = plaintext.ljust(8, b'\0')[:8]
        pt_int = int.from_bytes(pt_padded, 'big')
        
        ct_int = engine.encrypt(pt_int)
        
        return ct_int.to_bytes(8, 'big')

    def decrypt(self, ciphertext, key):
        return ciphertext