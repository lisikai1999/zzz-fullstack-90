import asyncio
import time
import uuid
from utils.progress_store import progress_store
from services.hash_service import quick_hash


async def start_birthday_attack(hash_bits: int) -> str:
    task_id = str(uuid.uuid4())
    progress_store[task_id] = {
        "status": "running",
        "attempts": 0,
        "hashes_stored": 0,
        "recent_hashes": [],
        "result": None,
        "start_time": time.time(),
        "hash_bits": hash_bits,
    }
    asyncio.create_task(_run_attack(task_id, hash_bits))
    return task_id


async def _run_attack(task_id: str, hash_bits: int):
    seen = {}
    attempts = 0
    recent = []

    try:
        while progress_store[task_id]["status"] == "running":
            msg = f"msg_{attempts}".encode('utf-8')
            h = quick_hash(msg, hash_bits)
            attempts += 1

            recent.append({"input": f"msg_{attempts-1}", "hash": h})
            if len(recent) > 10:
                recent = recent[-10:]

            if h in seen and seen[h] != msg:
                progress_store[task_id]["status"] = "complete"
                progress_store[task_id]["attempts"] = attempts
                progress_store[task_id]["hashes_stored"] = len(seen)
                progress_store[task_id]["recent_hashes"] = recent
                progress_store[task_id]["result"] = {
                    "input_1": seen[h].decode('utf-8'),
                    "input_2": msg.decode('utf-8'),
                    "hash_value": h,
                    "attempts_needed": attempts,
                }
                return

            seen[h] = msg

            if attempts % 50 == 0:
                progress_store[task_id]["attempts"] = attempts
                progress_store[task_id]["hashes_stored"] = len(seen)
                progress_store[task_id]["recent_hashes"] = list(recent)
                await asyncio.sleep(0)

    except Exception as e:
        progress_store[task_id]["status"] = "error"
        progress_store[task_id]["error"] = str(e)


def get_progress(task_id: str) -> dict:
    if task_id not in progress_store:
        return None
    entry = progress_store[task_id]
    elapsed = time.time() - entry["start_time"]
    return {
        "task_id": task_id,
        "status": entry["status"],
        "attempts": entry["attempts"],
        "hashes_stored": entry["hashes_stored"],
        "elapsed_seconds": round(elapsed, 2),
        "recent_hashes": entry["recent_hashes"],
    }


def get_result(task_id: str) -> dict:
    if task_id not in progress_store:
        return None
    entry = progress_store[task_id]
    hash_bits = entry["hash_bits"]
    theoretical = 2 ** (hash_bits // 2)
    return {
        "task_id": task_id,
        "status": entry["status"],
        "collision": entry["result"],
        "theoretical_expected": theoretical,
        "explanation": (
            f"对于 {hash_bits} 位哈希，生日悖论预测约 2^{hash_bits//2} = {theoretical} "
            f"次尝试后找到碰撞。实际用了 {entry['attempts']} 次。"
        ),
    }


def cancel_attack(task_id: str) -> bool:
    if task_id in progress_store:
        progress_store[task_id]["status"] = "cancelled"
        return True
    return False
