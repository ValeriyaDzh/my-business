from fastapi import APIRouter, Depends, status

from src.api.v1.services import SignInService
from src.schemas.signin import SignIn, SigninResponse

router = APIRouter()


@router.post("/sign-in", status_code=status.HTTP_200_OK, response_model=SigninResponse)
async def login_for_access_token(
    login_data: SignIn,
    signin_service: SignInService = Depends(SignInService),
) -> None:
    token = await signin_service.auth_and_create_token(
        login_data.email,
        login_data.password,
    )
    return SigninResponse(playload=token)


@router.get("/me")
async def get_me() -> None:
    return {"hello": "me"}
