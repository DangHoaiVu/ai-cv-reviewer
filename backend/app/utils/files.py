import base64
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.config import settings


def _looks_like_pdf(data: bytes) -> bool:
    return data.startswith(b"%PDF-") or data.startswith(b"JVBERi0")


async def save_pdf(upload: UploadFile) -> str:
    filename = upload.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Chỉ chấp nhận tệp PDF.")
    if upload.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Định dạng tệp không hợp lệ.")

    data = await upload.read(settings.max_upload_bytes + 1)
    if data.startswith(b"JVBERi0"):
        try:
            data = base64.b64decode(data)
        except Exception:
            pass

    if len(data) > settings.max_upload_bytes:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Tệp PDF không được vượt quá 10 MB.")
    if not data or not _looks_like_pdf(data):
        prefix_debug = data[:100].hex()
        preview_text = data[:100].decode('utf-8', errors='ignore')
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Tệp không phải là PDF hợp lệ. Prefix (Hex): {prefix_debug} | Text: {preview_text}"
        )

    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    file_id = uuid4().hex
    (settings.upload_dir / f"{file_id}.pdf").write_bytes(data)
    return file_id


def resolve_pdf(file_id: str) -> Path:
    path = settings.upload_dir / f"{file_id}.pdf"
    if not path.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Không tìm thấy CV. Vui lòng tải lên lại.")
    return path
