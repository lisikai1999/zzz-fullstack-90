from fastapi import APIRouter, HTTPException
from schemas.dh import DhExchangeRequest, DhMitmRequest, ColorMixingRequest
from services.dh_service import compute_exchange_steps, compute_mitm_steps, compute_color_mixing

router = APIRouter()


@router.post("/exchange")
def dh_exchange(req: DhExchangeRequest):
    if req.p < 2:
        raise HTTPException(status_code=400, detail="p 必须是大于 1 的素数")
    if req.g < 2 or req.g >= req.p:
        raise HTTPException(status_code=400, detail="g 必须满足 2 ≤ g < p")
    if req.a_private < 1 or req.a_private >= req.p:
        raise HTTPException(status_code=400, detail="私钥 a 需满足 1 ≤ a < p")
    if req.b_private < 1 or req.b_private >= req.p:
        raise HTTPException(status_code=400, detail="私钥 b 需满足 1 ≤ b < p")
    return compute_exchange_steps(req.p, req.g, req.a_private, req.b_private)


@router.post("/mitm")
def dh_mitm(req: DhMitmRequest):
    if req.p < 2:
        raise HTTPException(status_code=400, detail="p 必须是大于 1 的素数")
    return compute_mitm_steps(req.p, req.g, req.a_private, req.b_private, req.m_private)


@router.post("/color-mixing")
def color_mixing(req: ColorMixingRequest):
    try:
        result = compute_color_mixing(req.alice_private_color, req.bob_private_color, req.common_color)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
