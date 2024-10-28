from pydantic import BaseModel, EmailStr, field_validator

from src.utils.auth import Password


class Message(BaseModel):
    message: str


class SignUp(BaseModel):
    account: EmailStr


class VerifyEmail(BaseModel):
    account: EmailStr
    invite_token: int


class SignUpComplete(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str

    @field_validator("password", mode="after")
    def hash_password(cls, value: str) -> str:
        hashed_password = Password.hash(value)
        return hashed_password
