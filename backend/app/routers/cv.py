from fastapi import APIRouter, File, UploadFile

from app.schemas import ReviewRequest, ReviewResponse, UploadResponse
from app.services.gemini_service import review_resume
from app.services.pdf_service import extract_text
from app.utils.files import resolve_pdf, save_pdf

router = APIRouter(prefix="/api", tags=["CV"])


@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_cv(file: UploadFile = File(...)) -> UploadResponse:
    return UploadResponse(fileId=await save_pdf(file))


@router.post("/review", response_model=ReviewResponse)
async def review_cv(payload: ReviewRequest) -> ReviewResponse:
    path = resolve_pdf(payload.fileId)
    try:
        text = extract_text(path)
        return await review_resume(text)
    finally:
        path.unlink(missing_ok=True)
