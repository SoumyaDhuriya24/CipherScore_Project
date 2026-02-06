from pydantic import BaseModel
from typing import Optional, Any, Dict, List

class AuditRequestStandard(BaseModel):
    algorithm_name: str
    rounds: Optional[int] = 1000

class AuditRequestCustom(BaseModel):
    code: str
    rounds: Optional[int] = 1000

class VerificationRequest(BaseModel):
    code: str
    test_msg: str
    test_key: str

class VerificationResponse(BaseModel):
    output: str
    success: bool
    error: Optional[str] = None
