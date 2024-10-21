from src.utils.unit_of_work import UnitOfWork


class BaseService:

    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()
