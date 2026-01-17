from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    role: str
    username: str
    password: str
    avatar_url: str | None = None
    email: str | None = None
    is_active: bool


class UpdateUserProfileRequest(BaseModel):
    profile: dict | None = None


class AddUserRequest(BaseModel):
    username: str
    role: str
    gender: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
