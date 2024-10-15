from typing import Any

from src.utils.unit_of_work import UnitOfWork, transaction_mode


class BaseService:

    base_repository: str

    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()
