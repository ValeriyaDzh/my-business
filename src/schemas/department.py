from pydantic import BaseModel
from sqlalchemy_utils import LtreeType
import uuid

from src.models import Department


class Department(BaseModel):
    id: int | None
    name: str
    company_id: uuid.UUID
    parent_id: int | None

    class Config:
        from_attributes = True
