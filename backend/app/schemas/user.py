from enum import Enum

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    citizen = "citizen"
    authority = "authority"
    field_staff = "field_staff"
    admin = "admin"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.citizen


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
