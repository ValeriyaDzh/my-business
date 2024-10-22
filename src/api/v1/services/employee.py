import logging

from src.schemas.employee import CreateEmployee
from src.utils.auth import Password, TokenService
from src.utils.mail_util import MailService, mail_service
from src.utils.exceptions import (
    AlreadyExistsException,
    DatabaseException,
    ForbiddenException,
)
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


logger = logging.getLogger(__name__)


class EmployeeService(BaseService):

    def __init__(self):
        super().__init__()
        self.token_service: TokenService = TokenService()
        self.mail: MailService = mail_service

    async def create_and_send_invite(
        self, playload: CreateEmployee, admin: bool, company: str
    ) -> None:

        if admin:
            await self.create(playload, company)

            inv_token = self.token_service.create_access_token(
                {
                    "email": playload.email,
                    "company_id": company,
                }
            )
            inv_url = f"http://127.0.0.1:8000/api/v1/employees/registration/{inv_token}"

            await self.mail.send_invite_email(
                playload.email, playload.password, inv_url
            )
        else:
            raise ForbiddenException("Don't have enough rights to make changes")

    @transaction_mode
    async def create(self, playload: CreateEmployee, company: str) -> None:

        if await self.uow.user_repository.get_by_email(playload.email):
            raise AlreadyExistsException("This email is already in use")

        new_employee = playload.model_dump() | {"company_id": company}
        new_employee["hashed_password"] = Password.hash(new_employee.pop("password"))
        logger.debug(f"n_emp: {new_employee}")

        try:
            await self.uow.user_repository.add_one_and_get_obj(**new_employee)
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise DatabaseException
