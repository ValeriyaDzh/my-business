from datetime import date
from enum import Enum as PEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.schemas.task import TaskSchema

if TYPE_CHECKING:
    from src.models import User


class TaskStatus(PEnum):
    ASSIGNED = "ASSIGNED"
    IN_WORK = "IN_WORK"
    DONE = "DONE"


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    author: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
    )
    responsible: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
    )
    deadline: Mapped[date]
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.ASSIGNED,
    )
    estimated_time: Mapped[int]
    observers: Mapped[list["User"] | None] = relationship(
        backref="observed_tasks", secondary="task_observers_link",
    )
    executors: Mapped[list["User"] | None] = relationship(
        backref="executed_tasks", secondary="task_executors_link",
    )

    def to_pydantic_schema(self) -> TaskSchema:
        return TaskSchema(**self.__dict__)


class TaskObserversLink(Base):
    __tablename__ = "task_observers_link"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE"), primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True,
    )


class TaskExecutorsLink(Base):
    __tablename__ = "task_executors_link"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE"), primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True,
    )
