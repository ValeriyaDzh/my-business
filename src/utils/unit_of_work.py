from collections.abc import AsyncGenerator
from functools import wraps
from types import TracebackType
from typing import TYPE_CHECKING, Any

from src.database import async_session_maker
from src.repositories import CompanyRepository, DepartmentRepository, UserRepository
from src.utils.custom_types import AsyncFunc

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session: AsyncSession = self.session_factory()
        self.company_repository = CompanyRepository(self.session)
        self.department_repository = DepartmentRepository(self.session)
        self.user_repository = UserRepository(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
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
