from functools import wraps
from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.repositories import CompanyRepository, UserRepository
from src.utils.custom_types import AsyncFunc


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.company_repository = CompanyRepository(self.session)
        self.user_repository = UserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork() as uow:
        yield uow


def transaction_mode(func: AsyncFunc) -> AsyncFunc:

    @wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper