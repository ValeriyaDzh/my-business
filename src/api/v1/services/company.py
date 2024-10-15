from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class CompanyService(BaseService):

    base_repository: str = "company"

    @transaction_mode
    async def create(self, name: str) -> None:
        await self.uow.company_repository.add_one_and_get_id(company_name=name)
