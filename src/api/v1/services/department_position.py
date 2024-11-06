import logging

from src.models import Department, Position
from src.schemas.base import Message
from src.utils.exceptions import DatabaseException
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

logger = logging.getLogger(__name__)


class DepartmentPositionService(BaseService):

    @transaction_mode
    async def add_position(self, department: Department, position: Position) -> Message:

        try:
            await self.uow.department_position_repository.add_one(
                department_id=department.id, position_id=position.id,
            )
            return Message(message="Position add to department")
        except Exception:
            raise DatabaseException

    @transaction_mode
    async def remove_position(self, department_id: int, position_id: int) -> None:
        await self.uow.department_position_repository.delete_by_query(
            department_id=department_id, position_id=position_id,
        )

    @transaction_mode
    async def get_positions(self, department: Department) -> None:
        logger.debug(f"Positions: { department.positions=}")
        return [position.to_pydantic_schema() for position in department.positions]
