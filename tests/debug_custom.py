from fastapi.testclient import TestClient
import sys
import os

# Add project root to sys.path so we can import backend.main
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app

client = TestClient(app)

def debug_audit_custom():
    code = """
class MyCipher:
    def encrypt(self, plaintext, key):
        return plaintext
"""
    payload = {"code": code, "rounds": 100}
    response = client.post("/audit/custom", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    debug_audit_custom()
