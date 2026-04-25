from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.schemas.candidate_schema import CandidateCreate, CandidateDetailResponse, CandidateResponse
from app.schemas.common_schema import MessageResponse
from app.services.candidate_service import CandidateService


router = APIRouter(prefix="/candidates", tags=["Candidates"])


def to_candidate_response(candidate) -> CandidateResponse:
    return CandidateResponse(
        id=candidate.id,
        name=candidate.name,
        email=candidate.email,
        phone=candidate.phone,
        skills=[s.strip() for s in (candidate.skills_text or "").split(",") if s.strip()],
        experience_years=candidate.experience_years,
        education=candidate.education,
        summary=candidate.summary,
        created_at=candidate.created_at,
    )


@router.post("", response_model=CandidateResponse, dependencies=[Depends(require_roles("Admin", "HR"))])
def create_candidate(payload: CandidateCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    candidate = CandidateService(db).create_candidate(payload)
    return to_candidate_response(candidate)


@router.get("", response_model=list[CandidateResponse], dependencies=[Depends(require_roles("Admin", "HR"))])
def list_candidates(
    db: Session = Depends(get_db),
    skills: str | None = Query(default=None, description="Comma separated skills"),
    min_experience: float | None = Query(default=None, ge=0),
    _=Depends(get_current_user),
):
    parsed_skills = [s.strip() for s in skills.split(",")] if skills else None
    rows = CandidateService(db).list_candidates(parsed_skills, min_experience)
    return [to_candidate_response(row) for row in rows]


@router.get("/{candidate_id}", response_model=CandidateDetailResponse, dependencies=[Depends(require_roles("Admin", "HR"))])
def candidate_detail(candidate_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    row = CandidateService(db).get_candidate_detail(candidate_id)
    return CandidateDetailResponse(
        **to_candidate_response(row).model_dump(),
        resumes=[{"id": r.id, "file_path": r.file_path, "uploaded_at": r.uploaded_at.isoformat()} for r in row.resumes],
    )


@router.post(
    "/{candidate_id}/resume",
    response_model=MessageResponse,
    dependencies=[Depends(require_roles("Admin", "HR"))],
)
def upload_resume(
    candidate_id: int,
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    CandidateService(db).upload_resume(candidate_id, resume_file)
    return MessageResponse(message="Resume uploaded and parsed successfully")

