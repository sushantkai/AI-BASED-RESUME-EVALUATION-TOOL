from sqlalchemy.orm import Session

from app.models.match import Match
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.job_repository import JobRepository
from app.repositories.match_repository import MatchRepository
from app.services.ai_service import AIService


class MatchingService:
    def __init__(self, db: Session):
        self.candidate_repository = CandidateRepository(db)
        self.job_repository = JobRepository(db)
        self.match_repository = MatchRepository(db)
        self.ai_service = AIService()

    def run_matching(self, candidate_id: int | None = None, job_id: int | None = None) -> list[Match]:
        candidates = [self.candidate_repository.get_by_id(candidate_id)] if candidate_id else self.candidate_repository.list_all()
        jobs = [self.job_repository.get_by_id(job_id)] if job_id else self.job_repository.list_all()
        candidates = [c for c in candidates if c is not None]
        jobs = [j for j in jobs if j is not None]

        results: list[Match] = []
        for candidate in candidates:
            candidate_skills = self._skills_to_set(candidate.skills_text)
            for job in jobs:
                required_skills = self._skills_to_set(job.skills_text)
                if not required_skills:
                    skill_match_pct = 0.0
                else:
                    matching_count = len(candidate_skills.intersection(required_skills))
                    skill_match_pct = (matching_count / len(required_skills)) * 100

                required_experience = max(job.experience_required, 0.1)
                experience_match_pct = min((candidate.experience_years / required_experience) * 100, 100.0)
                overall_score = round((0.7 * skill_match_pct) + (0.3 * experience_match_pct), 2)

                explanation = self.ai_service.generate_match_explanation(
                    candidate_name=candidate.name,
                    job_title=job.title,
                    matching_skills=sorted(candidate_skills.intersection(required_skills)),
                    missing_skills=sorted(required_skills - candidate_skills),
                    experience_match_pct=experience_match_pct,
                )
                match = Match(
                    candidate_id=candidate.id,
                    job_id=job.id,
                    skill_match_pct=round(skill_match_pct, 2),
                    experience_match_pct=round(experience_match_pct, 2),
                    overall_score=overall_score,
                    explanation=explanation,
                )
                results.append(self.match_repository.upsert(match))
        return results

    def candidate_view(self, candidate_id: int):
        return self.match_repository.list_by_candidate(candidate_id)

    def job_view(self, job_id: int):
        return self.match_repository.list_by_job(job_id)

    def _skills_to_set(self, skills_text: str | None) -> set[str]:
        return {s.strip().lower() for s in (skills_text or "").split(",") if s.strip()}

