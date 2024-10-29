import uuid

from pydantic import BaseModel


class Department(BaseModel):
    id: int | None
    name: str
    company_id: uuid.UUID
    parent_id: int | None

    class Config:
        from_attributes = True


class DepartmentUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None

    class Config:
        from_attributes = True
