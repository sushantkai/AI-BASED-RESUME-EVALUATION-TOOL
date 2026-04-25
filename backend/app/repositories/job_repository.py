from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.job import Job


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job: Job) -> Job:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_by_id(self, job_id: int) -> Job | None:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def list_all(self) -> list[Job]:
        return self.db.query(Job).order_by(desc(Job.created_at)).all()

    def update(self, job: Job) -> Job:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def delete(self, job: Job) -> None:
        self.db.delete(job)
        self.db.commit()

    def recent(self, limit: int = 5) -> list[Job]:
        return self.db.query(Job).order_by(desc(Job.created_at)).limit(limit).all()

