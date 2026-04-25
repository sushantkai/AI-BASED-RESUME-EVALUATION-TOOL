from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.match import Match


class MatchRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, payload: Match) -> Match:
        existing = (
            self.db.query(Match)
            .filter(Match.candidate_id == payload.candidate_id, Match.job_id == payload.job_id)
            .first()
        )
        if existing:
            existing.skill_match_pct = payload.skill_match_pct
            existing.experience_match_pct = payload.experience_match_pct
            existing.overall_score = payload.overall_score
            existing.explanation = payload.explanation
            self.db.add(existing)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        self.db.add(payload)
        self.db.commit()
        self.db.refresh(payload)
        return payload

    def list_by_candidate(self, candidate_id: int) -> list[Match]:
        return (
            self.db.query(Match)
            .filter(Match.candidate_id == candidate_id)
            .order_by(desc(Match.overall_score))
            .all()
        )

    def list_by_job(self, job_id: int) -> list[Match]:
        return self.db.query(Match).filter(Match.job_id == job_id).order_by(desc(Match.overall_score)).all()

