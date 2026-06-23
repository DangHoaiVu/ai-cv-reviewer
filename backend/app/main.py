import sys
from pathlib import Path

# Add backend directory to sys.path to resolve imports correctly on Vercel
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.cv import router as cv_router

app = FastAPI(title="AI CV Reviewer API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(cv_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
