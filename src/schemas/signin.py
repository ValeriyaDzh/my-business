from pydantic import BaseModel, EmailStr, field_validator

from src.utils.auth import Password


class SignIn(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
