from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    fileId: str


class ReviewRequest(BaseModel):
    fileId: str = Field(pattern=r"^[0-9a-f]{32}$")


class ReviewResponse(BaseModel):
    score: int = Field(ge=0, le=100)
    strengths: list[str]
    weaknesses: list[str]
    missingSkills: list[str]
    suggestions: list[str]
    suitableRoles: list[str]
