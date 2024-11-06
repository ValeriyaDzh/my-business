from pydantic import BaseModel, EmailStr

from src.schemas.base import BaseResponse


class SignIn(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class SigninResponse(BaseResponse):
    playload: Token
