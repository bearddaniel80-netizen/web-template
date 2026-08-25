import os
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

INTERNAL_API_KEY = Path(
    "/run/secrets/fastapi_internal_key"
).read_text().strip()


@app.get("/health")
async def health():
    return {"status": "ok"}


def verify_internal_key(
    x_internal_key: str | None,
):
    if x_internal_key != INTERNAL_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )


@app.get("/api/data")
async def get_data(
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)

    return {
        "message": "Hello from FastAPI"
    }