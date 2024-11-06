import logging
from collections.abc import Sequence
from uuid import UUID

from src.models import Position
from src.schemas.position import PositionSchema
from src.utils.exceptions import AlreadyExistsException
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

logger = logging.getLogger(__name__)


class PositionService(BaseService):

    @transaction_mode
    async def create(self, name: str, company_id: UUID) -> PositionSchema:
        if await self.uow.position_repository.get_by_field("name", name):
            raise AlreadyExistsException

        new_position: Position = await self.uow.position_repository.add_one_and_get_obj(
            name=name, company_id=company_id,
        )
        return new_position.to_pydantic_schema()

    @transaction_mode
    async def get_all(self, company_id: UUID) -> Sequence[PositionSchema]:
        positions: Sequence[Position] = await self.uow.position_repository.get_by_field(
            "company_id", company_id, _all=True,
        )
        return [position.to_pydantic_schema() for position in positions]

    @transaction_mode
    async def get_by_id(self, position_id: int) -> Position | None:
        return await self.uow.position_repository.get_by_field("id", position_id)

    @transaction_mode
    async def update(self, position_id: int, new_name: str) -> PositionSchema:
        updated_position: Position = (
            await self.uow.position_repository.update_one_by_id(
                position_id, name=new_name,
            )
        )
        return updated_position.to_pydantic_schema()

    @transaction_mode
    async def delete(self, position_id: int) -> None:
        await self.uow.position_repository.delete_by_query(id=position_id)
