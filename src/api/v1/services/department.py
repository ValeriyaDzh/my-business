import logging
from collections.abc import Sequence
from uuid import UUID

from src.models import Department
from src.schemas.department import DepartmentUpdateRequest
from src.utils.exceptions import NotFoundException
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

logger = logging.getLogger(__name__)


class DepartmentService(BaseService):

    @transaction_mode
    async def create(
        self,
        company_id: UUID,
        name: str,
        parent_department: Department | None = None,
    ) -> Department:

        new_department = await self.uow.department_repository.add_one_and_get_obj(
            name=name,
            company_id=company_id,
            parent=parent_department,
        )
        return new_department.to_pydantic_schema()

    @transaction_mode
    async def get_all(self, company_id) -> Sequence[Department]:
        departments = await self.uow.department_repository.get_by_field(
            "company_id",
            company_id,
            _all=True,
        )
        return [department.to_pydantic_schema() for department in departments]

    @transaction_mode
    async def get_subdepartments(
        self,
        department: Department,
    ) -> Sequence[Department]:

        return await self.uow.department_repository.get_children(department.path)

    @transaction_mode
    async def delete(self, department: Department) -> None:

        parent_path = (
            str(department.path).rsplit(".", 1)[0] if department.parent_id else None
        )
        logger.debug(f"Here: {parent_path=}")

        await self.uow.department_repository.update_path(parent_path, department.path)

        await self.uow.department_repository.update_by_parent_id(
            department.id,
            parent_id=department.parent_id,
        )

        await self.uow.department_repository.delete_by_query(id=department.id)

    @transaction_mode
    async def update(
        self,
        # company_id: UUID,
        # department_id: int,
        department: Department,
        data: DepartmentUpdateRequest,
    ) -> Department:

        playload = data.model_dump(exclude_none=True)
        if data.parent_id:
            parent: Department = await self.uow.department_repository.get_by_field(
                "id",
                data.parent_id,
            )
            if not parent or parent.company_id != department.company_id:
                raise NotFoundException("Department not found")

            new_parent_path = parent.path + str(department.id)
            logger.debug(f"Here: {new_parent_path=}")

            await self.uow.department_repository.update_path(
                new_parent_path,
                department.path,
            )
            playload.update({"path": new_parent_path})

        updated_department: Department = (
            await self.uow.department_repository.update_one_by_id(
                department.id,
                **playload,
            )
        )
        return updated_department.to_pydantic_schema()

    @transaction_mode
    async def get_by_id(self, department_id: int) -> Department:
        return await self.uow.department_repository.get_by_field("id", department_id)
