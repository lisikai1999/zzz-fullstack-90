from pydantic import BaseModel
from typing import List, Optional


class DhExchangeRequest(BaseModel):
    p: int
    g: int
    a_private: int
    b_private: int


class DhMitmRequest(BaseModel):
    p: int
    g: int
    a_private: int
    b_private: int
    m_private: int


class ColorMixingRequest(BaseModel):
    alice_private_color: str
    bob_private_color: str
    common_color: str


class DhStep(BaseModel):
    step_number: int
    actor: str
    title: str
    expression: str
    explanation: str
    result: Optional[int] = None
    sub_steps: Optional[List[dict]] = None


class DhExchangeResponse(BaseModel):
    steps: List[DhStep]
    shared_secret: int
    security_note: str


class ColorMixingResponse(BaseModel):
    common_color: str
    alice: dict
    bob: dict
    explanation: str
    animation_keyframes: List[dict]
