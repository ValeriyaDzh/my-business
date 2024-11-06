from src.models import TaskObserversLink
from src.utils.repository import SqlAlchemyRepository


class TaskObserversRepository(SqlAlchemyRepository):

    model: TaskObserversLink = TaskObserversLink
