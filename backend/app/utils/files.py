from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.config import settings


def _looks_like_pdf(data: bytes) -> bool:
    return data.startswith(b"%PDF-")


async def save_pdf(upload: UploadFile) -> str:
    filename = upload.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Chỉ chấp nhận tệp PDF.")
    if upload.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Định dạng tệp không hợp lệ.")

    data = await upload.read(settings.max_upload_bytes + 1)
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Tệp PDF không được vượt quá 10 MB.")
    if not data or not _looks_like_pdf(data):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tệp không phải là PDF hợp lệ.")

    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    file_id = uuid4().hex
    (settings.upload_dir / f"{file_id}.pdf").write_bytes(data)
    return file_id


def resolve_pdf(file_id: str) -> Path:
    path = settings.upload_dir / f"{file_id}.pdf"
    if not path.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Không tìm thấy CV. Vui lòng tải lên lại.")
    return path
