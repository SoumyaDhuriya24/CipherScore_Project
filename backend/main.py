from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os
import importlib.util

# Add project root to path to allow importing core and ciphers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import CipherAuditAgent
from core.loader import load_custom_cipher_from_text
from ciphers.test_cipher import SimpleXORCipher
from ciphers.ascon_cipher import AsconCipher
from ciphers.simon_cipher import SimonCipher
from ciphers.speck_cipher import SpeckCipher
from ciphers.present_cipher import PresentCipher
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CipherScore API", description="Backend for CipherScore Security Evaluator")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---

class CipherOption(BaseModel):
    id: str
    name: str
    description: str

class AuditRequest(BaseModel):
    cipher_id: str
    custom_code: Optional[str] = None
    rounds: int = 1000

class AuditResponse(BaseModel):
    cipher_name: str
    report: Dict[str, Any]

# --- CIPHER MAPPING ---

AVAILABLE_CIPHERS = {
    "xor": {"name": "Simple XOR (Test)", "class": SimpleXORCipher},
    "ascon": {"name": "Ascon-128 (NIST Standard)", "class": AsconCipher},
    "simon": {"name": "Simon-64/128 (NSA Lightweight)", "class": SimonCipher},
    "speck": {"name": "Speck-64/128 (Software Optimized)", "class": SpeckCipher},
    "present": {"name": "PRESENT-80 (ISO Standard)", "class": PresentCipher},
    "custom": {"name": "✨ Custom (Paste Code)", "class": None}
}

# --- API ENDPOINTS ---

@app.get("/ciphers", response_model=List[CipherOption])
async def get_ciphers():
    """Returns a list of available ciphers."""
    ciphers = []
    for cid, info in AVAILABLE_CIPHERS.items():
        ciphers.append(CipherOption(id=cid, name=info["name"], description=info["name"]))
    return ciphers

@app.post("/audit", response_model=AuditResponse)
async def run_audit(request: AuditRequest):
    """Runs a cipher audit based on the selected cipher and parameters."""
    target_cipher = None
    
    try:
        if request.cipher_id == "custom":
            if not request.custom_code:
                raise HTTPException(status_code=400, detail="Custom code is required for custom cipher option.")
            try:
                target_cipher = load_custom_cipher_from_text(request.custom_code)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Compilation Error: {str(e)}")
        
        elif request.cipher_id in AVAILABLE_CIPHERS:
            cipher_class = AVAILABLE_CIPHERS[request.cipher_id]["class"]
            if cipher_class:
                target_cipher = cipher_class()
            else:
                raise HTTPException(status_code=500, detail="Cipher class not found.")
        else:
            raise HTTPException(status_code=404, detail="Cipher ID not found.")

        # Run Audit
        agent = CipherAuditAgent(target_cipher)
        report = agent.run_full_audit(rounds=request.rounds)
        
        return AuditResponse(cipher_name=target_cipher.name, report=report)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "CipherScore API is running"}

if __name__ == "__main__":
    import uvicorn
    # Run the app using uvicorn when executed directly
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
