from pydantic import BaseModel, Field, model_validator


class IssueCreate(BaseModel):
    title: str
    description: str
    category: str
    priority: str = "medium"
    severity: str = "medium"
    location: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @model_validator(mode="after")
    def validate_coordinate_pair(self):
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError(
                "Latitude and longitude must be provided together"
            )
        return self



class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    priority: str
    severity: str
    status: str
    location: str | None=None
    latitude: float | None = None
    longitude: float | None = None
    reported_by: int
    assigned_to: int | None = None

    class Config:
        from_attributes = True
