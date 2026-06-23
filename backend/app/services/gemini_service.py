import json
import re

import httpx
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.config import settings
from app.schemas import ReviewResponse

SYSTEM_PROMPT = """You are a professional technical recruiter and ATS specialist.
Analyze the resume fairly based only on its content. Return concise, actionable feedback.
Return exactly one JSON object with this schema:
{
  "score": integer from 0 to 100,
  "strengths": string[],
  "weaknesses": string[],
  "missingSkills": string[],
  "suggestions": string[],
  "suitableRoles": string[]
}
Do not include markdown or claims not supported by the resume. Write feedback in Vietnamese."""


def _parse_response(raw: str) -> ReviewResponse:
    candidate = raw.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", candidate, re.DOTALL)
    if fenced:
        candidate = fenced.group(1)
    try:
        return ReviewResponse.model_validate(json.loads(candidate))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "AI trả về kết quả không hợp lệ. Vui lòng thử lại.") from exc


async def review_resume(resume_text: str) -> ReviewResponse:
    if not settings.gemini_api_key:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Backend chưa được cấu hình GEMINI_API_KEY.",
        )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent"
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": f"RESUME CONTENT:\n{resume_text}"}]}],
        "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"},
    }
    
    headers = {}
    params = {}
    if settings.gemini_api_key.startswith("AIzaSy"):
        params["key"] = settings.gemini_api_key
    else:
        headers["Authorization"] = f"Bearer {settings.gemini_api_key}"

    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(url, params=params, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        raw = data["candidates"][0]["content"]["parts"][0]["text"]
    except httpx.HTTPStatusError as exc:
        err_body = exc.response.text
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY,
            f"Lỗi từ Gemini (HTTP {exc.response.status_code}): {err_body}"
        ) from exc
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY,
            f"Không thể nhận kết quả từ Gemini. Lỗi: {str(exc)}"
        ) from exc
    return _parse_response(raw)
