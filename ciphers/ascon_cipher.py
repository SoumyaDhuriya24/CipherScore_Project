# ciphers/ascon_cipher.py
import ascon
from core.interfaces import BaseCipher

class AsconCipher(BaseCipher):
    @property
    def name(self):
        return "Ascon-128 (NIST Standard)"

    def encrypt(self, plaintext, key):
        # Ascon requires a nonce (number used once). 
        # For benchmarking, we can use a fixed nonce or generate one.
        nonce = b'0'*16 
        associated_data = b'' 
        
        # Ensure key is 16 bytes for Ascon-128
        if len(key) != 16:
            # Pad or trim key for demo purposes
            key = key.ljust(16, b'\x00')[:16]
            
        return ascon.encrypt(key, nonce, associated_data, plaintext)

    def decrypt(self, ciphertext, key):
        nonce = b'0'*16
        associated_data = b''
        if len(key) != 16:
            key = key.ljust(16, b'\x00')[:16]
            
        return ascon.decrypt(key, nonce, associated_data, ciphertext)