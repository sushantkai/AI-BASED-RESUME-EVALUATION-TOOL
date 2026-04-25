from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (UniqueConstraint("candidate_id", "job_id", name="uq_candidate_job"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_match_pct: Mapped[float] = mapped_column(Float, nullable=False)
    experience_match_pct: Mapped[float] = mapped_column(Float, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    candidate = relationship("Candidate", back_populates="matches")
    job = relationship("Job", back_populates="matches")

