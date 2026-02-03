import sys
import io
import inspect

def load_custom_cipher_from_text(code_string):
    """
    Dynamically executes a string of Python code and returns a usable Cipher Object.
    Now includes smart detection for common initialization errors.
    """
    local_scope = {}
    
    try:
        # 1. Execute the code string safely
        exec(code_string, globals(), local_scope)
        
        # 2. Find the Class
        target_class = None
        for name, obj in local_scope.items():
            if isinstance(obj, type):
                # Check if it has an encrypt method (our only strict requirement)
                if hasattr(obj, 'encrypt'):
                    target_class = obj
                    break
        
        if target_class is None:
            raise ValueError("No class with an 'encrypt' method found. Please define a class.")

        # 3. Intelligent Instantiation (The Fix for your Error)
        try:
            # Try to create an instance: cipher = MyCipher()
            return target_class()
        except TypeError as e:
            # Check if the error is about missing arguments in __init__
            if "__init__" in str(e) and "missing" in str(e):
                raise ValueError(
                    f"⚠️ Compatibility Error: Your class '{target_class.__name__}' requires arguments in `__init__`.\n\n"
                    "👉 FIX: Remove the `__init__` method (or make it empty) and move your setup logic "
                    "into the `encrypt(self, plaintext, key)` method."
                )
            # Re-raise other errors (like syntax errors)
            raise e
            
    except Exception as e:
        # Pass the specific error message back to the UI
        raise ValueError(f"{e}")