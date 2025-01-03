from fastapi import APIRouter, Depends, status
from pydantic import EmailStr

from src.api.v1.dependencies import valid_user
from src.api.v1.services import SignupService
from src.schemas.base import BaseCreateResponse, BaseMessageResponse
from src.schemas.signup import (
    SignUpCompleteRequest,
    VerifyEmailRequest,
    VerifyEmailResponse,
)

router = APIRouter()


@router.get(
    "/check_account/{account}/",
    status_code=status.HTTP_200_OK,
    response_model=BaseMessageResponse,
)
async def check_account(
    account: EmailStr,
    signup_service: SignupService = Depends(SignupService),
) -> None:
    message = await signup_service.check_and_send_invate(account)
    return BaseMessageResponse(playload=message)


@router.post(
    "/sign-up/",
    status_code=status.HTTP_200_OK,
    response_model=VerifyEmailResponse,
)
async def sign_up(
    email_token: VerifyEmailRequest,
    signup_service: SignupService = Depends(SignupService),
) -> None:
    token = signup_service.verify_and_create_token(
        email_token.account,
        email_token.invite_token,
    )
    return VerifyEmailResponse(playload=token)


@router.post(
    "/sign-up-complete/",
    status_code=status.HTTP_201_CREATED,
    response_model=BaseCreateResponse,
)
async def sign_up_complete(
    data: SignUpCompleteRequest,
    email: str = Depends(valid_user),
    signup_service: SignupService = Depends(SignupService),
) -> None:
    await signup_service.create_company_and_admin(email, data)
    return BaseCreateResponse
