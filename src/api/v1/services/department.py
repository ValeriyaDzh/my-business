import logging
from collections.abc import Sequence

from src.models import Department
from src.schemas.department import DepartmentUpdate
from src.utils.exceptions import ForbiddenException, NotFoundException
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

logger = logging.getLogger(__name__)


class DepartmentService(BaseService):

    @transaction_mode
    async def create(
        self,
        company_id: str,
        admin: bool,
        name: str,
        parent_id: int | None = None,
    ) -> Department:

        if not admin:
            raise ForbiddenException("Don't have enough rights to make changes")

        if parent_id:
            parent: Department = await self.uow.department_repository.get_by_field(
                "id",
                parent_id,
            )
            logger.debug(parent)
            if parent and str(parent.company_id) == company_id:
                parent_id = parent
                logger.debug(parent_id)
            else:
                raise NotFoundException("Department not found")

        return await self.uow.department_repository.add_one_and_get_obj(
            name=name,
            company_id=company_id,
            parent=parent_id,
        )

    @transaction_mode
    async def get_all(self, company_id) -> Sequence[Department]:
        return await self.uow.department_repository.get_by_field(
            "company_id",
            company_id,
            _all=True,
        )

    @transaction_mode
    async def get_subdepartments(
        self,
        company_id: str,
        admin: bool,
        department_id: int,
    ) -> Sequence[Department]:
        if not admin:
            raise ForbiddenException("Don't have enough rights to make changes")

        department: Department = await self.uow.department_repository.get_by_field(
            "id",
            department_id,
        )
        if not department or str(department.company_id) != company_id:
            raise NotFoundException("Department not found")

        return await self.uow.department_repository.get_children(department.path)

    @transaction_mode
    async def delete(self, company_id: str, admin: bool, department_id: int) -> None:
        if not admin:
            raise ForbiddenException("Don't have enough rights to make changes")

        department: Department = await self.uow.department_repository.get_by_field(
            "id",
            department_id,
        )
        if not department or str(department.company_id) != company_id:
            raise NotFoundException("Department not found")

        parent_path = (
            str(department.path).rsplit(".", 1)[0] if department.parent_id else None
        )
        logger.debug(f"Here: {parent_path=}")

        await self.uow.department_repository.update_path(parent_path, department.path)

        await self.uow.department_repository.update_by_parent_id(
            department.id,
            parent_id=department.parent_id,
        )

        await self.uow.department_repository.delete_by_query(id=department_id)

    @transaction_mode
    async def update(
        self,
        company_id: str,
        admin: bool,
        department_id: int,
        data: DepartmentUpdate,
    ) -> Department:
        if not admin:
            raise ForbiddenException("Don't have enough rights to make changes")

        department: Department = await self.uow.department_repository.get_by_field(
            "id",
            department_id,
        )
        if not department or str(department.company_id) != company_id:
            raise NotFoundException("Department not found")

        playload = data.model_dump(exclude_none=True)
        if data.parent_id:
            parent: Department = await self.uow.department_repository.get_by_field(
                "id",
                data.parent_id,
            )
            if not parent or str(parent.company_id) != company_id:
                raise NotFoundException("Department not found")

            new_parent_path = parent.path + str(department_id)
            logger.debug(f"Here: {new_parent_path=}")

            await self.uow.department_repository.update_path(
                new_parent_path,
                department.path,
            )
            playload.update({"path": new_parent_path})

        return await self.uow.department_repository.update_one_by_id(
            department_id,
            **playload,
        )
