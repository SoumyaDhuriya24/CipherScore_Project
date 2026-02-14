# ciphers/simon_speck_logic.py

# --- SIMON CIPHER LOGIC (64/128 configuration) ---
class SimonCipherEngine:
    def __init__(self, key):
        self.word_size = 32  # 64-bit block = 2x 32-bit words
        self.rounds = 44     # Standard for Simon 64/128
        self.mask = (1 << self.word_size) - 1
        
        # Simple key schedule for demonstration
        # (Real Simon key schedule is complex, this suffices for avalanche tests)
        self.key_schedule = []
        k_val = int.from_bytes(key[:8], 'big') 
        for i in range(self.rounds):
            self.key_schedule.append((k_val + i) & self.mask)

    def encrypt(self, plaintext_int):
        # Split 64-bit block into two 32-bit words
        x = (plaintext_int >> self.word_size) & self.mask
        y = plaintext_int & self.mask
        
        for k in self.key_schedule:
            # Simon Round:
            # tmp = x;
            # x = y ^ (ROL(x, 1) & ROL(x, 8)) ^ ROL(x, 2) ^ k;
            # y = tmp;
            
            tmp = x
            # Circular shifts
            rol1 = ((x << 1) | (x >> (self.word_size - 1))) & self.mask
            rol8 = ((x << 8) | (x >> (self.word_size - 8))) & self.mask
            rol2 = ((x << 2) | (x >> (self.word_size - 2))) & self.mask
            
            x = y ^ (rol1 & rol8) ^ rol2 ^ k
            y = tmp
            
        return (x << self.word_size) | y

# --- SPECK CIPHER LOGIC (64/128 configuration) ---
class SpeckCipherEngine:
    def __init__(self, key):
        self.word_size = 32
        self.rounds = 27
        self.mask = (1 << self.word_size) - 1
        
        # Simplified key schedule for demo
        self.key_schedule = []
        k_val = int.from_bytes(key[:8], 'big')
        for i in range(self.rounds):
            self.key_schedule.append((k_val ^ i) & self.mask)

    def encrypt(self, plaintext_int):
        x = (plaintext_int >> self.word_size) & self.mask
        y = plaintext_int & self.mask
        
        for k in self.key_schedule:
            # Speck Round:
            # x = (ROR(x, 8) + y) ^ k
            # y = ROL(y, 3) ^ x
            
            # Rotate Right 8
            ror8 = ((x >> 8) | (x << (self.word_size - 8))) & self.mask
            x = (ror8 + y) & self.mask
            x ^= k
            
            # Rotate Left 3
            rol3 = ((y << 3) | (y >> (self.word_size - 3))) & self.mask
            y = rol3 ^ x

        return (x << self.word_size) | y