from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import Field


class JobStatus(str, Enum):
    PENDING = "Pending"
    APPLIED = "Applied"
    REJECTED = "Rejected"
    GHOSTED = "Ghosted"
    INTERVIEW = "Interview"
    CLOSED = "Closed"


class JobApplication(BaseModel):
    userid: int
    source: Optional[str] = "web"
    description: Optional[str] = None
    date_applied: Optional[datetime] = datetime.now()
    status: Optional[JobStatus] = Field("Applied", description="The status of the job")
    job_title: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateJobStatus(BaseModel):
    id: str

    class UpdateJobStatus(BaseModel):
        id: str
        status: JobStatus = Field(..., description="The status of the job")
