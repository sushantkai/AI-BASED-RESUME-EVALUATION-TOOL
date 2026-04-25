from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.job import Job
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.job_repository import JobRepository


class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.candidate_repository = CandidateRepository(db)
        self.job_repository = JobRepository(db)

    def get_dashboard_data(self) -> dict:
        total_candidates = self.db.query(Candidate).count()
        total_jobs = self.db.query(Job).count()
        recent_candidates = [
            {"id": c.id, "name": c.name, "created_at": c.created_at.isoformat()} for c in self.candidate_repository.recent()
        ]
        recent_jobs = [{"id": j.id, "title": j.title, "created_at": j.created_at.isoformat()} for j in self.job_repository.recent()]

        return {
            "total_candidates": total_candidates,
            "total_jobs": total_jobs,
            "recent_candidates": recent_candidates,
            "recent_jobs": recent_jobs,
        }

