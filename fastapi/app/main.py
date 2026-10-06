from .security.api_key_check import verify_internal_key
from .routers.minio import router as minio_router

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# Routers
# --------------------------------------------------

app.include_router(minio_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/data")
async def get_data(
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)

    return {
        "message": "Hello from FastAPI"
    }



