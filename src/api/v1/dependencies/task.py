import logging

from fastapi import Depends, Request

from src.api.v1.services import TaskService
from src.models import Task
from src.utils.exceptions import ForbiddenException, NotFoundException

logger = logging.getLogger(__name__)


async def valid_task_to_read(
    task_id: int,
    request: Request,
    department_service: TaskService = Depends(TaskService),
) -> Task:
    task: Task = await department_service.get_by_id(task_id)
    if not task or request.state.user.id not in (
        task.author,
        task.responsible,
        *[user.id for user in task.observers],
        *[user.id for user in task.executors],
    ):
        raise NotFoundException("Task not found")
    logger.debug(f"{task=}")
    return task


async def valid_task_to_edit(
    task_id: int,
    request: Request,
    department_service: TaskService = Depends(TaskService),
) -> Task:
    task: Task = await department_service.get_by_id(task_id)
    if not task:
        raise NotFoundException("Task not found")

    if request.state.user.id == task.author:
        raise ForbiddenException("Can edit only author")
    logger.debug(f"{task=}")
    return task
