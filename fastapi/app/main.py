import os, uuid
from datetime import timedelta
from pathlib import Path
from pydantic import BaseModel

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from minio.error import S3Error

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

def read_secret(name: str) -> str:
    path = f"/run/secrets/{name}"

    if os.path.exists(path):
        return Path(path).read_text().strip()

    # Useful for local development outside Docker
    return os.environ[name]


MINIO_ACCESS_KEY = read_secret("minio_app_user")
MINIO_SECRET_KEY = read_secret("minio_app_password")
INTERNAL_API_KEY = read_secret("fastapi_internal_key")
MINIO_BUCKET = os.environ["MINIO_BUCKET"]
MINIO_ENDPOINT = "minio:9000"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)


def verify_internal_key(
    x_internal_key: str | None,
):
    if x_internal_key != INTERNAL_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

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

# --------------------------------------------------
# Request models
# --------------------------------------------------

class UploadUrlRequest(BaseModel):
    content_type: str
    filename: str


# --------------------------------------------------
# Generate presigned upload URL
# --------------------------------------------------

@app.post("/api/uploads")
def create_upload_url(
    file: UploadUrlRequest,
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    # Generate a unique object name.
    #
    # Example:
    #
    # uploads/550e8400-e29b-41d4-a716-446655440000.pdf

    extension = ""

    if "." in file.filename:
        extension = "." + file.filename.split(".")[-1]

    object_name = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )

    try:
        url = minio_client.presigned_put_object(
            bucket_name=MINIO_BUCKET,
            object_name=object_name,
            expires=timedelta(days=1),
        )

        return {
            "object_name": object_name,
            "url": url,
        }

    except S3Error as e:
        print(str(e))
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# --------------------------------------------------
# Generate download URL
# --------------------------------------------------

@app.get("/api/downloads/{object_name:path}")
def create_download_url(
    object_name: str,
):

    try:

        url = minio_client.presigned_get_object(
            MINIO_BUCKET,
            object_name,
            expires=timedelta(minutes=10),
        )

        return {
            "url": url,
        }

    except S3Error as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )