from pydantic import BaseModel, EmailStr

from src.schemas.base import BaseMessageCreateResponse, BaseMessageResponse


class Employee(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class CreateEmployee(Employee):
    password: str


class UpdateEmployee(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class EmploeeMessageResponse(BaseMessageResponse):
    pass


class EmploeeMessageCreateResponse(BaseMessageCreateResponse):
    pass
