from datetime import date
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.schemas.base import (
    BaseCreateResponse,
    BaseResponse,
)

if TYPE_CHECKING:
    from src.models import User


class TaskStatus(str, Enum):
    ASSIGNED = "ASSIGNED"
    IN_WORK = "IN_WORK"
    DONE = "DONE"


class Employee(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    author: UUID
    responsible: UUID
    deadline: date
    status: TaskStatus
    estimated_time: int
    observers: list[Employee] | None = []
    executors: list[Employee] | None = []

    class Config:
        from_attributes = True

    @field_validator("observers", mode="before")
    def observers_to_schema(cls, value: list["User"]) -> list["Employee"]:
        return [user.__dict__ for user in value]

    @field_validator("executors", mode="before")
    def executors_to_schema(cls, value: list["User"]) -> list["Employee"]:
        return [user.__dict__ for user in value]


class TaskBaseResponse(BaseResponse):
    playload: TaskSchema


class TaskListResponse(BaseResponse):
    playload: list[TaskSchema]


class TaskCreateRequest(BaseModel):
    title: str
    description: str
    deadline: date
    status: TaskStatus
    estimated_time: int
    observers: list[UUID] | None = []
    executors: list[UUID] | None = []

    class Config:
        from_attributes = True


class TaskCreateResponse(BaseCreateResponse):
    playload: TaskSchema


class TaskUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: date | None = None
    status: TaskStatus | None = None
    estimated_time: int | None = None
    observers: list[Employee] | None = []
    executors: list[Employee] | None = []

    class Config:
        from_attributes = True
