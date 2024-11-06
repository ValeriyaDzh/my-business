import logging
from uuid import UUID

from src.models import User
from src.utils.exceptions import DatabaseException, NotFoundException
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

logger = logging.getLogger(__name__)


class EmployeePositionService(BaseService):
    @transaction_mode
    async def appoint_employee(
        self, department_id: int, position_id: int, employee_id: UUID,
    ) -> User:

        try:
            appoined_employee: User = await self.uow.user_repository.update_one_by_id(
                employee_id, department_id=department_id, position_id=position_id,
            )
            return appoined_employee.to_pydantic_schema()
        except Exception:
            raise DatabaseException

    @transaction_mode
    async def remove_position(
        self, department_id: int, position_id: int, employee: User,
    ) -> None:

        if (
            employee.department_id == department_id
            and employee.position_id == position_id
        ):
            await self.uow.user_repository.update_one_by_id(
                employee.id, position_id=None, department_id=None,
            )

        raise NotFoundException("The employee does not belong to this position")
