import logging
from typing import TYPE_CHECKING

from sqlalchemy import select, func
from sqlalchemy_utils import Ltree

from src.models import Department
from src.utils.repository import SqlAlchemyRepository

if TYPE_CHECKING:
    from sqlalchemy.engine import Result

logger = logging.getLogger(__name__)


class DepartmentRepository(SqlAlchemyRepository):

    model: Department = Department

    async def add_one_and_get_obj(self, **kwargs):
        logger.debug(f"Data for department: {kwargs}")
        return await self.model.create(self.session, **kwargs)
