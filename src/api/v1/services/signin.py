from src.models.user import User
from src.schemas.signin import Token
from src.utils.auth import Password, TokenService
from src.utils.exceptions import UnauthorizedException
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class SignInService(BaseService):

    def __init__(self):
        super().__init__()
        self.token_service: TokenService = TokenService()

    async def auth_and_create_token(self, email: str, password: str) -> Token:
        user: User = await self.authentificate_user(email, password)

        access_token = self.token_service.create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "is_admin": user.is_admin,
                "company_id": str(user.company_id),
            },
        )
        return Token(access_token=access_token, token_type="Bearer")

    @transaction_mode
    async def authentificate_user(self, email: str, password: str) -> User:
        user = await self.uow.user_repository.get_by_email(email)

        if user and Password.verify(password, user.hashed_password):
            return user
        raise UnauthorizedException(detail="Incorrect login or password")

    @transaction_mode
    async def verified_user(self, current_user: User) -> None:
        await self.uow.user_repository.update_one_by_id(
            current_user.id, {"is_verified": True},
        )
