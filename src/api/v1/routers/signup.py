from fastapi import APIRouter, Depends, status
from pydantic import EmailStr

from src.schemas.signup import SignUp, Message, VerifyEmail
from src.api.v1.services import UserService, SignupService
from src.utils.mail_util import mail_service

router = APIRouter()


@router.get(
    "/check_account/{account}", status_code=status.HTTP_200_OK, response_model=Message
)
async def check_account(
    account: EmailStr,
    signup_service: SignupService = Depends(SignupService),
):
    await signup_service.check_and_send_invate(account)
    return Message(message="Registration confirmation code has been sent")


@router.post("/sign-up", status_code=status.HTTP_200_OK)
async def sign_up(
    email_token: VerifyEmail, signup_service: SignupService = Depends(SignupService)
):
    return signup_service.token_service.verify_signup_token(
        email_token.account, email_token.invite_token
    )
