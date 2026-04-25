from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_candidates: int
    total_jobs: int
    recent_candidates: list[dict]
    recent_jobs: list[dict]

