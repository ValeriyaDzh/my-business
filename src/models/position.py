from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, Department
from src.schemas.position import PositionSchema


class Position(Base):
    __tablename__ = "position"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    name: Mapped[str]
    company_id: Mapped[str] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"),
    )
    departments: Mapped[list["Department"]] = relationship(
        back_populates="positions", secondary="department_position_link"
    )

    def to_pydantic_schema(self) -> PositionSchema:
        return PositionSchema(**self.__dict__)
