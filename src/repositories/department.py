import logging

from src.models import Department
from src.utils.repository import SqlAlchemyRepository

logger = logging.getLogger(__name__)


class DepartmentRepository(SqlAlchemyRepository):

    model: Department = Department

    async def add_one_and_get_obj(self, **kwargs) -> Department:
        logger.debug(f"Data for department: {kwargs}")
        return await self.model.create(self.session, **kwargs)
