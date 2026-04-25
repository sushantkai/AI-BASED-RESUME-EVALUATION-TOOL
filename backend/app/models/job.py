from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    department: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    skills_text: Mapped[str] = mapped_column(Text, nullable=False)
    experience_required: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    improved_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    matches = relationship("Match", back_populates="job", cascade="all, delete-orphan")

