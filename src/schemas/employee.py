from pydantic import BaseModel, EmailStr

from src.utils.auth import Password


class Registration(BaseModel):
    password: str


class Employee(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class CreateEmployee(Employee):
    password: str
