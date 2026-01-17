from typing import Optional
from pydantic import BaseModel


class CreateDepartmentRequest(BaseModel):
    name: str
    parent_id: Optional[int] = None
    description: Optional[str] = None


class UpdateDepartmentRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
