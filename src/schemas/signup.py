from pydantic import BaseModel, EmailStr, field_validator

from src.schemas.base import BaseResponse
from src.schemas.signin import Token
from src.utils.auth import Password


class SignUp(BaseModel):
    account: EmailStr


class VerifyEmailRequest(BaseModel):
    account: EmailStr
    invite_token: int


class VerifyEmailResponse(BaseResponse):
    playload: Token


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


class SignUpCompleteRequest(BaseModel):
    password: str
    first_name: str
    last_name: str
    company_name: str

    @field_validator("password", mode="after")
    def hash_password(cls, value: str) -> str:
        hashed_password = Password.hash(value)
        return hashed_password
