from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.schemas.common_schema import MessageResponse
from app.schemas.job_schema import JobCreate, JobResponse, JobUpdate
from app.services.job_service import JobService


router = APIRouter(prefix="/jobs", tags=["Jobs"])


def to_job_response(job) -> JobResponse:
    return JobResponse(
        id=job.id,
        title=job.title,
        department=job.department,
        skills=[s.strip() for s in (job.skills_text or "").split(",") if s.strip()],
        experience_required=job.experience_required,
        description=job.description,
        improved_description=job.improved_description,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


@router.post("", response_model=JobResponse, dependencies=[Depends(require_roles("Admin", "HR"))])
def create_job(payload: JobCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return to_job_response(JobService(db).create_job(payload))


@router.get("", response_model=list[JobResponse], dependencies=[Depends(require_roles("Admin", "HR"))])
def list_jobs(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return [to_job_response(job) for job in JobService(db).list_jobs()]


@router.put("/{job_id}", response_model=JobResponse, dependencies=[Depends(require_roles("Admin", "HR"))])
def update_job(job_id: int, payload: JobUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return to_job_response(JobService(db).update_job(job_id, payload))


@router.delete("/{job_id}", response_model=MessageResponse, dependencies=[Depends(require_roles("Admin"))])
def delete_job(job_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    JobService(db).delete_job(job_id)
    return MessageResponse(message="Job deleted successfully")

