from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class DepartmentPositionLink(Base):
    __tablename__ = "department_position_link"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("department.id", ondelete="CASCADE"),
    )
    position_id: Mapped[int] = mapped_column(
        ForeignKey("position.id", ondelete="CASCADE"),
    )
