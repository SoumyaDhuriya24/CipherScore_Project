import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to path to import from core/ciphers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import CipherAuditAgent
from core.loader import load_custom_cipher_from_text
from ciphers.ascon_cipher import AsconCipher
from ciphers.simon_cipher import SimonCipher
from ciphers.speck_cipher import SpeckCipher
from ciphers.present_cipher import PresentCipher
from ciphers.test_cipher import SimpleXORCipher
from backend.models import AuditRequestStandard, AuditRequestCustom, VerificationRequest, VerificationResponse

app = FastAPI(title="CipherScore API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALGORITHMS = {
    "Ascon-128 (NIST)": AsconCipher,
    "Simon-64/128 (NSA)": SimonCipher,
    "Speck-64/128": SpeckCipher,
    "PRESENT-80": PresentCipher,
    "Simple XOR (Weak)": SimpleXORCipher
}

@app.get("/algorithms")
def get_algorithms():
    return list(ALGORITHMS.keys())

@app.post("/audit/standard")
def audit_standard(request: AuditRequestStandard):
    if request.algorithm_name not in ALGORITHMS:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    
    CipherClass = ALGORITHMS[request.algorithm_name]
    cipher_instance = CipherClass()
    
    try:
        agent = CipherAuditAgent(cipher_instance)
        report = agent.run_full_audit(rounds=request.rounds)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audit/custom")
def audit_custom(request: AuditRequestCustom):
    try:
        cipher_instance = load_custom_cipher_from_text(request.code)
        agent = CipherAuditAgent(cipher_instance)
        report = agent.run_full_audit(rounds=request.rounds)
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify/custom", response_model=VerificationResponse)
def verify_custom(request: VerificationRequest):
    try:
        cipher_instance = load_custom_cipher_from_text(request.code)
        # Encrypt
        res = cipher_instance.encrypt(request.test_msg.encode(), request.test_key.encode())
        output = res.hex().upper() if isinstance(res, bytes) else str(res)
        return VerificationResponse(output=output, success=True)
    except Exception as e:
        return VerificationResponse(output="", success=False, error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
