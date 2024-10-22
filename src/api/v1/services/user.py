import logging
from uuid import UUID

from src.models import User
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

logger = logging.getLogger(__name__)


class UserService(BaseService):

    @transaction_mode
    async def get_by_id(self, id: UUID) -> User | None:
        return await self.uow.user_repository.get_by_field("id", id)
