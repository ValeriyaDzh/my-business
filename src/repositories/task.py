from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import Task
from src.utils.repository import SqlAlchemyRepository

if TYPE_CHECKING:
    from sqlalchemy.engine import Result


class TaskRepository(SqlAlchemyRepository):

    model: Task = Task

    async def get_by_id_with_selectinload(self, obj_id: int) -> Task:
        query = (
            select(self.model)
            .where(self.model.id == obj_id)
            .options(selectinload(self.model.executors))
            .options(selectinload(self.model.observers))
        )
        res: Result = await self.session.execute(query)
        return res.scalar_one_or_none()
