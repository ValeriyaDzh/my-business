import logging

from src.models import Task, User
from src.schemas.task import TaskCreateRequest, TaskUpdateRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

logger = logging.getLogger(__name__)


class TaskService(BaseService):

    @transaction_mode
    async def create(self, author: User, data: TaskCreateRequest) -> Task:
        logger.debug(f"{data.status=}-{data.status.value=}")

        playload = data.model_dump()
        executors = playload.pop("executors")
        observers = playload.pop("observers")
        task: Task = await self.uow.task_repository.add_one_and_get_obj(
            **playload,
            author=author.id,
            responsible=author.id,
        )

        task_schema = task.to_pydantic_schema()

        if executors:
            for executor_id in data.executors:
                employee: User = await self.uow.user_repository.get_by_filters(
                    id=executor_id,
                )
                if employee and author.company_id == employee.company_id:
                    await self.uow.task_executors_repository.add_one(
                        task_id=task.id, user_id=employee.id,
                    )
                    task_schema.executors.append(employee)

        if observers:
            for observer_id in observers:
                employee: User = await self.uow.user_repository.get_by_filters(
                    id=observer_id,
                )
                if employee and author.company_id == employee.company_id:
                    await self.uow.task_observers_repository.add_one(
                        task_id=task.id, user_id=employee.id,
                    )
                    task_schema.observers.append(employee)

        return task_schema

    @transaction_mode
    async def update(self, task: Task, author: User, data: TaskUpdateRequest) -> Task:

        playload = data.model_dump()
        executors = playload.pop("executors")
        observers = playload.pop("observers")

        task: Task = await self.uow.task_repository.update_one_by_id(**playload)

        task_schema = task.to_pydantic_schema()

        if executors:
            await self.uow.task_executors_repository.delete_by_query(task_id=task.id)
            for executor_id in data.executors:
                employee: User = await self.uow.user_repository.get_by_filters(
                    id=executor_id,
                )
                if employee and author.company_id == employee.company_id:
                    await self.uow.task_executors_repository.add_one(
                        task_id=task.id, user_id=employee.id,
                    )
                    task_schema.executors.append(employee)

        if observers:
            await self.uow.task_observers_repository.delete_by_query(task_id=task.id)
            for observer_id in observers:
                employee: User = await self.uow.user_repository.get_by_filters(
                    id=observer_id,
                )
                if employee and author.company_id == employee.company_id:
                    await self.uow.task_observers_repository.add_one(
                        task_id=task.id, user_id=employee.id,
                    )
                    task_schema.observers.append(employee)

        return task_schema

    @transaction_mode
    async def delete(self, task_id: int) -> None:
        await self.uow.task_repository.delete_by_query(id=task_id)

    @transaction_mode
    async def get_by_id(self, task_id: int) -> Task:
        return await self.uow.task_repository.get_by_id_with_selectinload(task_id)

    # @transaction_mode
    # async def get_all(self, employee: User) -> Sequence[Task]:
    #     pass

    # @transaction_mode
    # async def get_observed(self, employee: User) -> Sequence[Task]:
    #     pass

    # @transaction_mode
    # async def get_executored(self, employee: User) -> Sequence[Task]:
    #     pass
