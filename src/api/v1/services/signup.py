import logging

from src.api.v1.services import UserService, CompanyService
from src.utils.auth import TokenService
from src.utils.exceptions import AlreadyExistsException
from src.utils.mail_util import MailService, mail_service

logger = logging.getLogger(__name__)


class SignupService:
    def __init__(self):
        self.user_service: UserService = UserService()
        self.company_service: CompanyService = CompanyService()
        self.token_service: TokenService = TokenService()
        self.mail_service: MailService = mail_service

    async def check_and_send_invate(self, email: str):

        if await self.user_service.get_by_email(email):
            raise AlreadyExistsException(detail="This email is already in use")

        token = self.token_service.generate_signup_token()
        try:
            await self.mail_service.send_verify_email(
                recipient=email, invite_token=token
            )
            self.token_service.save_signup_token(account=email, token=token)
        except Exception as e:
            logger.exception(f"Failed to send signup token: {e}")
