from fastapi import APIRouter, Depends, status
from pydantic import EmailStr

from src.api.v1.services import SignupService
from src.schemas.signup import Message, SignUpComplete, VerifyEmail

router = APIRouter()


@router.get(
    "/check_account/{account}/", status_code=status.HTTP_200_OK, response_model=Message,
)
async def check_account(
    account: EmailStr,
    signup_service: SignupService = Depends(SignupService),
):
    await signup_service.check_and_send_invate(account)
    return Message(message="Registration confirmation code has been sent")


@router.post("/sign-up/", status_code=status.HTTP_200_OK)
async def sign_up(
    email_token: VerifyEmail, signup_service: SignupService = Depends(SignupService),
):
    return signup_service.token_service.verify_signup_token(
        email_token.account, email_token.invite_token,
    )


@router.post(
    "auth/api/v1/sign-up-complete/",
    status_code=status.HTTP_201_CREATED,
    response_model=Message,
)
async def sign_up_complete(
    data: SignUpComplete, signup_service: SignupService = Depends(SignupService),
):
    await signup_service.create_company_and_admin(data)
    return Message(message="Done...")
