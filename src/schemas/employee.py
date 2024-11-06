from pydantic import BaseModel, EmailStr

from src.schemas.base import (
    BaseMessageCreateResponse,
    BaseMessageResponse,
    BaseResponse,
)


class EmployeeSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    department_id: int | None
    position_id: int | None


class CreateEmployee(EmployeeSchema):
    password: str


class UpdateEmployee(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    department_id: int | None = None
    position_id: int | None = None


class EmployeeBaseResponse(BaseResponse):
    playload: EmployeeSchema


class EmployeeListResponse(BaseResponse):
    playload: list[EmployeeSchema]


class EmployeeMessageResponse(BaseMessageResponse):
    pass


class EmployeeMessageCreateResponse(BaseMessageCreateResponse):
    pass
