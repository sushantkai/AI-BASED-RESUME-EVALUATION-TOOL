from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    department: str = Field(min_length=2, max_length=120)
    skills: list[str] = Field(min_length=1)
    experience_required: float = Field(ge=0)
    description: str = Field(min_length=5)


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    improved_description: str | None = None
    created_at: datetime
    updated_at: datetime

