from fastapi import APIRouter, HTTPException
from schemas.hash import (
    HashComputeRequest, BirthdayAttackStartRequest,
    BirthdayAttackStartResponse,
)
from services.hash_service import simplified_sha
from services.birthday_attack import start_birthday_attack, get_progress, get_result, cancel_attack

router = APIRouter()


@router.post("/compute")
def compute_hash(req: HashComputeRequest):
    if req.hash_bits < 8 or req.hash_bits > 64:
        raise HTTPException(status_code=400, detail="hash_bits 需在 8-64 之间")
    result = simplified_sha(req.message, req.hash_bits)
    return result


@router.post("/birthday-attack/start")
async def birthday_attack_start(req: BirthdayAttackStartRequest):
    if req.hash_bits < 8 or req.hash_bits > 32:
        raise HTTPException(status_code=400, detail="生日攻击 hash_bits 需在 8-32 之间")
    task_id = await start_birthday_attack(req.hash_bits)
    theoretical = 2 ** (req.hash_bits // 2)
    return BirthdayAttackStartResponse(
        task_id=task_id,
        hash_bits=req.hash_bits,
        estimated_attempts=theoretical,
    )


@router.get("/birthday-attack/{task_id}/progress")
def birthday_attack_progress(task_id: str):
    progress = get_progress(task_id)
    if progress is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return progress


@router.get("/birthday-attack/{task_id}/result")
def birthday_attack_result(task_id: str):
    result = get_result(task_id)
    if result is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return result


@router.delete("/birthday-attack/{task_id}")
def birthday_attack_cancel(task_id: str):
    if not cancel_attack(task_id):
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"status": "cancelled"}
