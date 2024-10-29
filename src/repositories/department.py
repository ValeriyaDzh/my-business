import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from sqlalchemy import and_, select, text, update
from sqlalchemy_utils import LtreeType

from src.models import Department
from src.utils.repository import SqlAlchemyRepository

if TYPE_CHECKING:
    from sqlalchemy.engine import Result

logger = logging.getLogger(__name__)


class DepartmentRepository(SqlAlchemyRepository):

    model: Department = Department

    async def add_one_and_get_obj(self, **kwargs: Any) -> Department:
        logger.debug(f"Data for department: {kwargs}")
        return await self.model.create(self.session, **kwargs)

    async def get_children(self, path: str) -> Sequence[Department] | None:
        res: Result = await self.session.execute(
            select(self.model).where(
                and_(self.model.path.op("<@")(path), self.model.path != path),
            ),
        )
        return res.scalars().all()

    async def update_path(self, parent_path: str, delete_path: LtreeType) -> None:
        query = (
            update(self.model)
            .where(
                and_(
                    self.model.path.op("<@")(delete_path),
                    self.model.path != delete_path,
                ),
            )
            .values(
                path=text(
                    f"'{parent_path or ''}' || subpath(path, nlevel('{delete_path!s}'))",
                ),
            )
        )
        await self.session.execute(query)

    async def update_by_parent_id(self, id: int, **kwargs: Any) -> None:
        query = update(self.model).filter(self.model.parent_id == id).values(**kwargs)
        await self.session.execute(query)
