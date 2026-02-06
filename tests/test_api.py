from fastapi.testclient import TestClient
import sys
import os

# Add project root to sys.path so we can import backend.main
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app

client = TestClient(app)

def test_get_algorithms():
    response = client.get("/algorithms")
    assert response.status_code == 200
    algos = response.json()
    assert "Ascon-128 (NIST)" in algos
    assert "Simple XOR (Weak)" in algos

def test_audit_standard():
    payload = {"algorithm_name": "Ascon-128 (NIST)", "rounds": 100}
    response = client.post("/audit/standard", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Avalanche Score" in data
    assert "Encryption Speed (ms)" in data

def test_audit_custom_valid():
    code = """
class MyCipher:
    def encrypt(self, plaintext, key):
        return plaintext
"""
    payload = {"code": code, "rounds": 100}
    response = client.post("/audit/custom", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Avalanche Score" in data

def test_verify_custom_success():
    code = """
class MyCipher:
    def encrypt(self, plaintext, key):
        return plaintext
"""
    payload = {
        "code": code,
        "test_msg": "test",
        "test_key": "key"
    }
    response = client.post("/verify/custom", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # In the dummy cipher, it returns plaintext "test" encoded hex likely?
    # Wait, the dummy cipher returns plaintext bytes or string.
    # The agent logic might expect bytes. 
    # Let's adjust the dummy cipher to be more robust for the test if needed.

def test_verify_custom_failure():
    code = """
class BrokenCipher:
    def encrypt(self, plaintext, key):
        raise ValueError("Boom")
"""
    payload = {
        "code": code,
        "test_msg": "test",
        "test_key": "key"
    }
    response = client.post("/verify/custom", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "Boom" in data["error"]
