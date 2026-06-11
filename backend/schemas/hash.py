from pydantic import BaseModel
from typing import List, Optional


class HashComputeRequest(BaseModel):
    message: str
    hash_bits: int = 16


class RoundState(BaseModel):
    round_number: int
    W_i: str
    K_i: str
    state_before: dict
    state_after: dict
    operations: dict


class BlockResult(BaseModel):
    block_index: int
    block_data_hex: str
    rounds: List[RoundState]
    chain_value_after: str


class HashComputeResponse(BaseModel):
    final_hash: str
    hash_bits: int
    message_hex: str
    padding_explanation: str
    blocks: List[BlockResult]


class BirthdayAttackStartRequest(BaseModel):
    hash_bits: int = 16


class BirthdayAttackStartResponse(BaseModel):
    task_id: str
    hash_bits: int
    estimated_attempts: int


class BirthdayAttackProgress(BaseModel):
    task_id: str
    status: str
    attempts: int
    hashes_stored: int
    elapsed_seconds: float
    recent_hashes: List[dict]


class BirthdayAttackResult(BaseModel):
    task_id: str
    status: str
    collision: Optional[dict] = None
    theoretical_expected: int
    explanation: str
