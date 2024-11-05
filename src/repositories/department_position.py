from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from sqlalchemy import delete, select
from sqlalchemy_utils import LtreeType

from src.models import DepartmentPositionLink
from src.utils.repository import SqlAlchemyRepository

if TYPE_CHECKING:
    from sqlalchemy.engine import Result


class DepartmentPositionRepository(SqlAlchemyRepository):

    model: DepartmentPositionLink = DepartmentPositionLink
