import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING

from src.schemas.department import Department, DepartmentCreate
from src.repositories import DepartmentRepository
from src.utils.exceptions import (
    AlreadyExistsException,
    ForbiddenException,
    NotFoundException,
)
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
            # department: Department = await self.uow.department_repository.get_by_field(
            #     "name", name
            # )
            # if department and department.company_id == company_id:
            #     raise AlreadyExistsException("Department is already in use")
            # new_path = await self.uow.department_repository.get_ltree_path()
            # logger.debug(f"path: {new_path}")

            if parent_id:
                parent: Department = await self.uow.department_repository.get_by_field(
                    "id", parent_id
                )
                logger.debug(parent)
                if parent and str(parent.company_id) == company_id:
                    # new_path = await self.uow.department_repository.get_ltree_path(
                    #     parent.path
                    # )
                    parent_id = parent
                    logger.debug(parent_id)
                else:
                    raise NotFoundException("Department not found")

            data = DepartmentCreate(
                name=name, company_id=company_id, parent=parent_id
            ).model_dump(exclude_none=True)

            logger.debug(f"New department data: {data}")
            # return await self.uow.department_repository.add_one_and_get_obj(
            #     **data, path=new_path
            # )
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
