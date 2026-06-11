from fastapi import APIRouter, HTTPException
from schemas.rsa import KeyGenRequest, KeyGenResponse, EncryptRequest, DecryptRequest, CryptoResponse
from services.rsa_service import generate_keys_with_steps, encrypt_with_steps, decrypt_with_steps

router = APIRouter()


@router.post("/generate-keys")
def generate_keys(req: KeyGenRequest):
    try:
        result = generate_keys_with_steps(req.p, req.q, req.e)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/encrypt")
def encrypt(req: EncryptRequest):
    try:
        result = encrypt_with_steps(req.message, req.e, req.n)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/decrypt")
def decrypt(req: DecryptRequest):
    try:
        result = decrypt_with_steps(req.ciphertext, req.d, req.n)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
