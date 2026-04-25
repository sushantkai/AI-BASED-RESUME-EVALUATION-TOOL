from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.resume import Resume


class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, candidate: Candidate) -> Candidate:
        self.db.add(candidate)
        self.db.commit()
        self.db.refresh(candidate)
        return candidate

    def get_by_id(self, candidate_id: int) -> Candidate | None:
        return self.db.query(Candidate).filter(Candidate.id == candidate_id).first()

    def get_by_email(self, email: str) -> Candidate | None:
        return self.db.query(Candidate).filter(Candidate.email == email).first()

    def list_all(self, skills: list[str] | None = None, min_experience: float | None = None) -> list[Candidate]:
        query = self.db.query(Candidate)
        if min_experience is not None:
            query = query.filter(Candidate.experience_years >= min_experience)
        rows = query.order_by(desc(Candidate.created_at)).all()
        if not skills:
            return rows
        normalized = {s.strip().lower() for s in skills if s.strip()}
        filtered = []
        for row in rows:
            row_skills = {s.strip().lower() for s in (row.skills_text or "").split(",") if s.strip()}
            if normalized.issubset(row_skills):
                filtered.append(row)
        return filtered

    def save_resume(self, resume: Resume) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def update(self, candidate: Candidate) -> Candidate:
        self.db.add(candidate)
        self.db.commit()
        self.db.refresh(candidate)
        return candidate

    def recent(self, limit: int = 5) -> list[Candidate]:
        return self.db.query(Candidate).order_by(desc(Candidate.created_at)).limit(limit).all()

