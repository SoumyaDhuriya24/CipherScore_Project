# core/loader.py
import sys
import io
from core.interfaces import BaseCipher

def load_custom_cipher_from_text(code_string):
    """
    Dynamically executes a string of Python code and returns the first class 
    that looks like a Cipher.
    """
    # 1. Create a restricted scope to run the code
    local_scope = {}
    
    try:
        # 2. Execute the string as Python code
        # Warning: exec() is dangerous in public web apps, but fine for local projects.
        exec(code_string, globals(), local_scope)
        
        # 3. Find the class that was defined in the code
        target_class = None
        
        for name, obj in local_scope.items():
            # Check if it's a class and has the required methods
            if isinstance(obj, type):
                # Check for 'encrypt' and 'decrypt' methods
                if hasattr(obj, 'encrypt') and hasattr(obj, 'decrypt'):
                    target_class = obj
                    break
        
        if target_class:
            return target_class() # Return an INSTANCE of the class
        else:
            raise ValueError("No valid Cipher class found. Did you define a class with encrypt/decrypt methods?")
            
    except Exception as e:
        raise ValueError(f"Code Error: {e}")