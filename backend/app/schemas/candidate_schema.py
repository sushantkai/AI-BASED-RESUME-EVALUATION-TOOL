from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CandidateBase(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=50)


class CandidateCreate(CandidateBase):
    pass


class CandidateResponse(CandidateBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    skills: list[str] = []
    experience_years: float = 0.0
    education: str | None = None
    summary: str | None = None
    created_at: datetime


class CandidateDetailResponse(CandidateResponse):
    resumes: list[dict] = []

