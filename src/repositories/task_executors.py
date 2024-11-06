from src.models import TaskExecutorsLink
from src.utils.repository import SqlAlchemyRepository


class TaskExecutorsRepository(SqlAlchemyRepository):

    model: TaskExecutorsLink = TaskExecutorsLink
