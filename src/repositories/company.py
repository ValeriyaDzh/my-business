from uuid import UUID

from src.models import Company
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):

    model = Company

    async def create_and_get_id(self, name: str) -> UUID:
        return await self.add_one_and_get_id(name=name)

    async def get_by_name(self, name: str) -> Company | None:
        return await self.get_by_field("name", name)
