from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories.ai_data_repository import AIDataRepository
from app.repositories.job_repository import JobRepository
from app.schemas.job_schema import JobCreate, JobUpdate
from app.services.ai_service import AIService


class JobService:
    def __init__(self, db: Session):
        self.job_repository = JobRepository(db)
        self.ai_repository = AIDataRepository(db)
        self.ai_service = AIService()

    def create_job(self, payload: JobCreate) -> Job:
        improved = self.ai_service.improve_job_description(
            title=payload.title,
            department=payload.department,
            description=payload.description,
            skills=payload.skills,
            experience_required=payload.experience_required,
        )
        job = Job(
            title=payload.title,
            department=payload.department,
            skills_text=", ".join(payload.skills),
            experience_required=payload.experience_required,
            description=payload.description,
            improved_description=improved,
        )
        created = self.job_repository.create(job)
        self.ai_repository.create("job", created.id, "improved_description", improved)
        return created

    def list_jobs(self) -> list[Job]:
        return self.job_repository.list_all()

    def get_job(self, job_id: int) -> Job:
        job = self.job_repository.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        return job

    def update_job(self, job_id: int, payload: JobUpdate) -> Job:
        job = self.get_job(job_id)
        job.title = payload.title
        job.department = payload.department
        job.skills_text = ", ".join(payload.skills)
        job.experience_required = payload.experience_required
        job.description = payload.description
        job.improved_description = self.ai_service.improve_job_description(
            title=payload.title,
            department=payload.department,
            description=payload.description,
            skills=payload.skills,
            experience_required=payload.experience_required,
        )
        updated = self.job_repository.update(job)
        self.ai_repository.create("job", updated.id, "improved_description", updated.improved_description or "")
        return updated

    def delete_job(self, job_id: int) -> None:
        job = self.get_job(job_id)
        self.job_repository.delete(job)

