from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.schemas.employee import EmployeeSchema
from src.utils.custom_types import uuid_pk


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid_pk]
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[str] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"),
    )
    department_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("department.id"),
    )
    position_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("position.id"))

    def to_pydantic_schema(self) -> EmployeeSchema:
        return EmployeeSchema(**self.__dict__)
