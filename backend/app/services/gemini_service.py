import json
import re
import httpx
from fastapi import HTTPException, status
from pydantic import ValidationError
from app.config import settings
from app.schemas import ReviewResponse

import os
from pathlib import Path
from google.oauth2 import service_account
import google.auth.transport.requests

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
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": f"RESUME CONTENT:\n{resume_text}"}]}],
        "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"},
    }
    
    headers = {}
    params = {}

    # Check for service-account.json in env variable, backend/ or project root/
    env_sa_json = os.getenv("GEMINI_SERVICE_ACCOUNT_JSON")
    backend_sa_path = Path(__file__).resolve().parent.parent.parent / "service-account.json"
    root_sa_path = Path(__file__).resolve().parent.parent.parent.parent / "service-account.json"
    
    creds = None
    project_id = None
    if env_sa_json:
        try:
            info = json.loads(env_sa_json)
            project_id = info.get("project_id")
            creds = service_account.Credentials.from_service_account_info(
                info,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        except Exception as exc:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                f"Lỗi nạp Service Account từ biến môi trường GEMINI_SERVICE_ACCOUNT_JSON: {str(exc)}"
            )
    elif backend_sa_path.is_file():
        try:
            with open(backend_sa_path, "r") as f:
                info = json.load(f)
                project_id = info.get("project_id")
            creds = service_account.Credentials.from_service_account_file(
                str(backend_sa_path),
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        except Exception as exc:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                f"Lỗi nạp Service Account từ file backend/service-account.json: {str(exc)}"
            )
    elif root_sa_path.is_file():
        try:
            with open(root_sa_path, "r") as f:
                info = json.load(f)
                project_id = info.get("project_id")
            creds = service_account.Credentials.from_service_account_file(
                str(root_sa_path),
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        except Exception as exc:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                f"Lỗi nạp Service Account từ file root/service-account.json: {str(exc)}"
            )

    if creds and project_id:
        # Route to Vertex AI endpoint when using Service Account
        url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/{settings.gemini_model}:generateContent"
        try:
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
            headers["Authorization"] = f"Bearer {creds.token}"
        except Exception as exc:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                f"Lỗi khi xác thực bằng Service Account: {str(exc)}"
            )
    else:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent"
        if not settings.gemini_api_key:
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "Backend chưa được cấu hình GEMINI_API_KEY hoặc file service-account.json.",
            )
        if settings.gemini_api_key.startswith(("AIzaSy", "AQ.")):
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
        if exc.response.status_code in (401, 403):
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                f"Lỗi xác thực Gemini API (HTTP {exc.response.status_code}). "
                f"Vui lòng kiểm tra hoặc cập nhật lại GEMINI_API_KEY trong file backend/.env. Chi tiết: {err_body}"
            ) from exc
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
