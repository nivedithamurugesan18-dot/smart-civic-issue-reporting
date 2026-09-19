from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class AssignmentCreate(BaseModel):
    issue_id: int
    assigned_to: int


class AssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    issue_id: int
    assigned_to: int
    assigned_by: int
    status: str
    assigned_at: datetime
    completed_at: Optional[datetime] = None