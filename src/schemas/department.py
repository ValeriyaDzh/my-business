import uuid

from pydantic import BaseModel


class Department(BaseModel):
    id: int | None
    name: str
    company_id: uuid.UUID
    parent_id: int | None

    class Config:
        from_attributes = True
