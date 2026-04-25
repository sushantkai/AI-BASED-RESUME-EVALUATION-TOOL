import os
import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.repositories.ai_data_repository import AIDataRepository
from app.repositories.candidate_repository import CandidateRepository
from app.schemas.candidate_schema import CandidateCreate
from app.services.ai_service import AIService


class CandidateService:
    def __init__(self, db: Session):
        self.candidate_repository = CandidateRepository(db)
        self.ai_data_repository = AIDataRepository(db)
        self.ai_service = AIService()

    def create_candidate(self, payload: CandidateCreate) -> Candidate:
        if self.candidate_repository.get_by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Candidate email already exists")
        candidate = Candidate(name=payload.name, email=payload.email, phone=payload.phone)
        return self.candidate_repository.create(candidate)

    def list_candidates(self, skills: list[str] | None, min_experience: float | None) -> list[Candidate]:
        return self.candidate_repository.list_all(skills=skills, min_experience=min_experience)

    def get_candidate_detail(self, candidate_id: int) -> Candidate:
        candidate = self.candidate_repository.get_by_id(candidate_id)
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
        return candidate

    def upload_resume(self, candidate_id: int, resume_file: UploadFile) -> Resume:
        candidate = self.get_candidate_detail(candidate_id)
        os.makedirs(settings.upload_dir, exist_ok=True)

        ext = os.path.splitext(resume_file.filename or "")[1] or ".txt"
        filename = f"{candidate_id}_{uuid.uuid4().hex}{ext}"
        path = os.path.join(settings.upload_dir, filename)

        raw_bytes = resume_file.file.read()
        with open(path, "wb") as output:
            output.write(raw_bytes)

        raw_text = self._extract_text(raw_bytes)
        resume = self.candidate_repository.save_resume(Resume(candidate_id=candidate_id, file_path=path, raw_text=raw_text))

        parsed = self.ai_service.parse_resume(raw_text)
        candidate.skills_text = ", ".join(parsed["skills"])
        candidate.experience_years = parsed["experience_years"]
        candidate.education = parsed["education"]
        candidate.summary = self.ai_service.generate_candidate_summary(
            candidate_name=candidate.name,
            skills=parsed["skills"],
            experience_years=parsed["experience_years"],
            education=parsed["education"],
        )
        self.candidate_repository.update(candidate)

        self.ai_data_repository.create("candidate", candidate.id, "resume_parse", str(parsed))
        self.ai_data_repository.create("candidate", candidate.id, "summary", candidate.summary or "")
        return resume

    def _extract_text(self, raw_bytes: bytes) -> str:
        try:
            return raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return raw_bytes.decode("latin-1", errors="ignore")

