import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING

from src.schemas.department import Department
from src.utils.exceptions import ForbiddenException, NotFoundException
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

if TYPE_CHECKING:
    from src.models import Department

logger = logging.getLogger(__name__)


class DepartmentService(BaseService):

    @transaction_mode
    async def create(
        self, company_id: str, admin: bool, name: str, parent_id: int | None = None
    ) -> Department:

        if admin:
            if parent_id:
                parent: Department = await self.uow.department_repository.get_by_field(
                    "id", parent_id
                )
                logger.debug(parent)
                if parent and str(parent.company_id) == company_id:
                    parent_id = parent
                    logger.debug(parent_id)
                else:
                    raise NotFoundException("Department not found")

            return await self.uow.department_repository.add_one_and_get_obj(
                name=name, company_id=company_id, parent=parent_id
            )

        else:
            raise ForbiddenException("Don't have enough rights to make changes")

    @transaction_mode
    async def get_all(self, company_id) -> Sequence[Department]:

        return await self.uow.department_repository.get_by_field(
            "company_id", company_id, _all=True
        )
