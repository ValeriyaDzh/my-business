from src.models import DepartmentPositionLink
from src.utils.repository import SqlAlchemyRepository


class DepartmentPositionRepository(SqlAlchemyRepository):

    model: DepartmentPositionLink = DepartmentPositionLink
