from pydantic import BaseModel, ConfigDict
from typing import Optional


class IssueImageCreate(BaseModel):
    issue_id: int
    image_url: str
    file_name: Optional[str] = None


class IssueImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    issue_id: int
    image_url: str
    file_name: Optional[str] = None