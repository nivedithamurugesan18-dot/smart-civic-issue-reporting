from datetime import datetime

from pydantic import BaseModel


# ============================================================
# CREATE ISSUE UPDATE
# ============================================================

class IssueUpdateCreate(BaseModel):
    message: str
    status: str | None = None


# ============================================================
# ISSUE UPDATE RESPONSE
# ============================================================

class IssueUpdateResponse(BaseModel):
    id: int
    issue_id: int
    updated_by: int
    message: str
    status: str | None
    created_at: datetime

    class Config:
        from_attributes = True
