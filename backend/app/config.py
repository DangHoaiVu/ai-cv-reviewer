import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()



@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    max_upload_bytes: int = 10 * 1024 * 1024
    upload_dir: Path = Path(os.getenv("UPLOAD_DIR", Path(tempfile.gettempdir()) / "ai-cv-reviewer"))
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")


settings = Settings()
