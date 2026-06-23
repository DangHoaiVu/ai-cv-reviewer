from pathlib import Path

import fitz
from fastapi import HTTPException, status


def extract_text(path: Path) -> str:
    try:
        with fitz.open(path) as document:
            text = "\n".join(page.get_text("text") for page in document)
    except (fitz.FileDataError, RuntimeError, ValueError) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Không thể đọc nội dung PDF.") from exc

    normalized = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if len(normalized) < 30:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "PDF không có đủ văn bản để phân tích. CV dạng ảnh chưa được hỗ trợ.",
        )
    return normalized[:50_000]
