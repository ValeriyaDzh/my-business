from pydantic import BaseModel, EmailStr


class Employee(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class CreateEmployee(Employee):
    password: str


class UpdateEmployee(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
