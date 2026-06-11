from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import rsa, hash, dh

app = FastAPI(title="密码学交互式教学平台", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rsa.router, prefix="/api/rsa", tags=["RSA"])
app.include_router(hash.router, prefix="/api/hash", tags=["Hash"])
app.include_router(dh.router, prefix="/api/dh", tags=["Diffie-Hellman"])


@app.on_event("startup")
def startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok"}
