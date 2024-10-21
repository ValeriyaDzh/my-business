import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base

if TYPE_CHECKING:
    from sqlalchemy.engine import Result

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Base)


class SqlAlchemyRepository:

    model: type[T] = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, **kwargs: Any) -> None:
        query = insert(self.model).values(**kwargs)
        await self.session.execute(query)

    async def add_one_and_get_obj(self, **kwargs: Any) -> T:
        query = insert(self.model).values(**kwargs).returning(self.model)
        obj: Result = await self.session.execute(query)
        return obj.scalar_one()

    async def add_one_and_get_id(self, **kwargs: Any) -> T:
        query = insert(self.model).values(**kwargs).returning(self.model.id)
        obj: Result = await self.session.execute(query)
        return obj.scalar_one()

    async def get_by_field(
        self,
        key: str,
        value: str,
        _all: bool = False,
    ) -> T | Sequence[T] | None:
        query = select(self.model).where(and_(getattr(self.model, key) == value))
        res: Result = await self.session.execute(query)

        if _all:
            return res.scalars().all()

        return res.scalar_one_or_none()

    async def update_one_by_id(self, obj_id: UUID, **kwargs: Any) -> T | None:
        query = (
            update(self.model)
            .filter(self.model.id == obj_id)
            .values(**kwargs)
            .returning(self.model)
        )
        res: Result | None = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def delete_by_query(self, **kwargs: Any) -> None:
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)
