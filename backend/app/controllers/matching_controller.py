from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.schemas.match_schema import CandidateMatchView, JobMatchView, MatchResponse
from app.services.matching_service import MatchingService


router = APIRouter(prefix="/matches", tags=["Matches"])


def to_match_response(match) -> MatchResponse:
    return MatchResponse(
        id=match.id,
        candidate_id=match.candidate_id,
        job_id=match.job_id,
        skill_match_pct=match.skill_match_pct,
        experience_match_pct=match.experience_match_pct,
        overall_score=match.overall_score,
        explanation=match.explanation,
        created_at=match.created_at,
    )


@router.post("/run", response_model=list[MatchResponse], dependencies=[Depends(require_roles("Admin", "HR"))])
def run_matching(
    candidate_id: int | None = Query(default=None),
    job_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    rows = MatchingService(db).run_matching(candidate_id=candidate_id, job_id=job_id)
    return [to_match_response(row) for row in rows]


@router.get("/candidate/{candidate_id}", response_model=list[CandidateMatchView], dependencies=[Depends(require_roles("Admin", "HR"))])
def candidate_view(candidate_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    rows = MatchingService(db).candidate_view(candidate_id)
    return [
        CandidateMatchView(
            candidate_id=row.candidate_id,
            candidate_name=row.candidate.name,
            job_id=row.job_id,
            job_title=row.job.title,
            skill_match_pct=row.skill_match_pct,
            experience_match_pct=row.experience_match_pct,
            overall_score=row.overall_score,
            explanation=row.explanation,
        )
        for row in rows
    ]


@router.get("/job/{job_id}", response_model=list[JobMatchView], dependencies=[Depends(require_roles("Admin", "HR"))])
def job_view(job_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    rows = MatchingService(db).job_view(job_id)
    return [
        JobMatchView(
            job_id=row.job_id,
            job_title=row.job.title,
            candidate_id=row.candidate_id,
            candidate_name=row.candidate.name,
            overall_score=row.overall_score,
            skill_match_pct=row.skill_match_pct,
            experience_match_pct=row.experience_match_pct,
            explanation=row.explanation,
        )
        for row in rows
    ]

