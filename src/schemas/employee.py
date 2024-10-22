from pydantic import BaseModel, EmailStr, field_validator

from src.utils.auth import Password


class Employee(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class CreateEmployee(Employee):
    password: str
