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
    if not settings.openrouter_api_key:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Backend chưa được cấu hình OPENROUTER_API_KEY.",
        )

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"RESUME CONTENT:\n{resume_text}"}
        ],
        "response_format": {"type": "json_object"}
    }
    
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/DangHoaiVu/ai-cv-reviewer",
        "X-Title": "AI CV Reviewer"
    }

    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        raw = data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as exc:
        err_body = exc.response.text
        if exc.response.status_code in (401, 403):
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                f"Lỗi xác thực OpenRouter API (HTTP {exc.response.status_code}). "
                f"Vui lòng kiểm tra lại OPENROUTER_API_KEY trong file backend/.env. Chi tiết: {err_body}"
            ) from exc
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY,
            f"Lỗi từ OpenRouter (HTTP {exc.response.status_code}): {err_body}"
        ) from exc
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY,
            f"Không thể nhận kết quả từ OpenRouter. Lỗi: {str(exc)}"
        ) from exc
    return _parse_response(raw)
