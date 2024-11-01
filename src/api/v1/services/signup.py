import logging

from src.schemas.base import Message
from src.schemas.signin import Token
from src.schemas.signup import SignUpComplete
from src.utils.auth import TokenService
from src.utils.exceptions import (
    AlreadyExistsException,
    DatabaseException,
    UnauthorizedException,
)
from src.utils.mail_util import MailService, mail_service
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

logger = logging.getLogger(__name__)


class SignupService(BaseService):
    def __init__(self):
        super().__init__()
        self.token_service: TokenService = TokenService()
        self.mail_service: MailService = mail_service

    @transaction_mode
    async def check_and_send_invate(self, email: str) -> Message:

        if await self.uow.user_repository.get_by_email(email):
            raise AlreadyExistsException(detail="This email is already in use")

        token = self.token_service.generate_signup_token()
        try:
            await self.mail_service.send_verify_email(
                recipient=email,
                invite_token=token,
            )
            self.token_service.save_signup_token(account=email, token=token)
            return Message(message="Registration confirmation code has been sent")
        except Exception as e:
            logger.exception(f"Failed to send signup token: {e}")

    def verify_and_create_token(self, email: str, token: int) -> Token:
        if self.token_service.verify_signup_token(email, token):
            access_token = self.token_service.create_access_token(
                {
                    "email": email,
                },
            )
            return Token(access_token=access_token, token_type="Bearer")
        raise UnauthorizedException

    @transaction_mode
    async def create_company_and_admin(self, playload: SignUpComplete) -> None:
        try:
            if await self.uow.company_repository.get_by_field(
                "name",
                playload.company_name,
            ):
                raise AlreadyExistsException("Company with this name is already exist")

            company_id = await self.uow.company_repository.add_one_and_get_id(
                name=playload.company_name,
            )
            logger.debug(f"Created company {playload.company_name} - {company_id}")

            data_dict = playload.model_dump()
            del data_dict["company_name"]
            data_dict["hashed_password"] = data_dict.pop("password")
            data_dict["email"] = data_dict.pop("account")
            logger.debug(f"Prepared user: {data_dict}")

            created_user = await self.uow.user_repository.add_one_and_get_obj(
                **data_dict,
                is_admin=True,
                company_id=company_id,
                is_verified=True,
            )
            logger.debug(created_user)

        except AlreadyExistsException:
            raise
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise DatabaseException
