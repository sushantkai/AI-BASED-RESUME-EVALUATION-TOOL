from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    skills_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    experience_years: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    education: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    resumes = relationship("Resume", back_populates="candidate", cascade="all, delete-orphan")
    matches = relationship("Match", back_populates="candidate", cascade="all, delete-orphan")

