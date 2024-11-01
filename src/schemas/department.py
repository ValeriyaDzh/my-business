from uuid import UUID

from pydantic import BaseModel

from src.schemas.base import BaseCreateResponse, BaseResponse


class DepartmentSchema(BaseModel):
    id: int | None
    name: str
    company_id: UUID
    parent_id: int | None

    class Config:
        from_attributes = True


class DepartmentCreateResponse(BaseCreateResponse):
    playload: DepartmentSchema


class DepartmentUpdateRequest(BaseModel):
    name: str | None = None
    parent_id: int | None = None

    class Config:
        from_attributes = True


class DepartmentResponse(BaseResponse):
    payload: DepartmentSchema


class DepartmentListResponse(BaseResponse):
    payload: list[DepartmentSchema]
