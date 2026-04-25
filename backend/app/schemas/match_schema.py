from datetime import datetime

from pydantic import BaseModel


class MatchResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    skill_match_pct: float
    experience_match_pct: float
    overall_score: float
    explanation: str | None
    created_at: datetime


class CandidateMatchView(BaseModel):
    candidate_id: int
    candidate_name: str
    job_id: int
    job_title: str
    skill_match_pct: float
    experience_match_pct: float
    overall_score: float
    explanation: str | None


class JobMatchView(BaseModel):
    job_id: int
    job_title: str
    candidate_id: int
    candidate_name: str
    overall_score: float
    skill_match_pct: float
    experience_match_pct: float
    explanation: str | None

