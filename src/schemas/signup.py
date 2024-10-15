from pydantic import BaseModel, EmailStr


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
