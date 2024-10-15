import logging
from typing import TYPE_CHECKING

from src.models import User
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


if TYPE_CHECKING:
    from src.models import User

logger = logging.getLogger(__name__)


class UserService(BaseService):

    base_repository: str = "user"

    @transaction_mode
    async def get_by_email(self, email: str) -> User | None:
        user = await self.uow.user_repository.get_by_field("email", email)
        return user
