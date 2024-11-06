from fastapi import APIRouter, Depends, Request, status

from src.api.v1.dependencies import valid_task_to_edit, valid_task_to_read
from src.api.v1.services import TaskService
from src.models import Task
from src.schemas.task import (
    TaskBaseResponse,
    TaskCreateRequest,
    TaskCreateResponse,
    TaskListResponse,
    TaskUpdateRequest,
)

router = APIRouter()


@router.get(
    "/tasks",
    status_code=status.HTTP_200_OK,
    response_model=TaskListResponse,
)
async def get_tasks(
    request: Request,
    task_service: TaskService = Depends(TaskService),
) -> None:
    tasks = await task_service.get_all(request.state.user)
    return TaskListResponse(playload=tasks)


@router.get(
    "/tasks/task/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskBaseResponse,
)
async def get_task(
    task: Task = Depends(valid_task_to_read),
) -> None:
    return TaskBaseResponse(playload=task)


@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskCreateResponse,
)
async def create_task(
    request: Request,
    task_data: TaskCreateRequest,
    task_service: TaskService = Depends(TaskService),
) -> None:
    task = await task_service.create(request.state.user, task_data)
    return TaskCreateResponse(playload=task)


@router.patch(
    "/tasks/task/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskBaseResponse,
)
async def update_task(
    task_data: TaskUpdateRequest,
    request: Request,
    task: Task = Depends(valid_task_to_read),
    task_service: TaskService = Depends(TaskService),
) -> None:
    task = await task_service.update(task, request.state.user, task_data)
    return TaskBaseResponse(playload=task)


@router.delete(
    "/tasks/task/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task: Task = Depends(valid_task_to_edit),
    task_service: TaskService = Depends(TaskService),
) -> None:
    await task_service.delete(task.id)
