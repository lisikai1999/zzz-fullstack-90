from pydantic import BaseModel
from typing import List, Optional


class Step(BaseModel):
    step_number: int
    title: str
    expression: str
    explanation: str
    intermediate_value: Optional[int] = None
    bit: Optional[int] = None
    operation: Optional[str] = None
    sub_steps: Optional[List[dict]] = None


class KeyGenRequest(BaseModel):
    p: int
    q: int
    e: Optional[int] = None


class KeyGenResponse(BaseModel):
    steps: List[Step]
    public_key: dict
    private_key: dict
    parameters: dict


class EncryptRequest(BaseModel):
    message: int
    e: int
    n: int


class DecryptRequest(BaseModel):
    ciphertext: int
    d: int
    n: int


class CryptoResponse(BaseModel):
    result: int
    steps: List[Step]
    summary: dict
