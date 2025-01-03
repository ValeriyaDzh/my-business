from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Integer, Sequence, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship, remote
from sqlalchemy_utils import Ltree, LtreeType

from src.models import Base
from src.schemas.department import DepartmentSchema

if TYPE_CHECKING:
    from sqlalchemy.engine import Result

    from src.models import Position

id_seq = Sequence("department_id_seq")


class Department(Base):
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(Integer, id_seq, primary_key=True)
    name: Mapped[str]
    path: Mapped[str] = mapped_column(LtreeType)
    company_id: Mapped[str] = mapped_column(ForeignKey("company.id"))
    parent_id: Mapped[int] = mapped_column(ForeignKey("department.id"), nullable=True)
    head_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id"))

    positions: Mapped[list["Position"]] = relationship(
        back_populates="departments", secondary="department_position_link",
    )

    parent = relationship(
        "Department",
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref="children",
        viewonly=True,
    )

    __table_args__ = (Index("ix_departments_path", path, postgresql_using="gist"),)

    @classmethod
    async def create(
        cls,
        async_session: AsyncSession,
        name: str,
        company_id: str,
        parent: Optional["Department"] = None,
    ) -> Optional["Department"]:
        result: Result = await async_session.execute(select(id_seq.next_value()))
        _id = result.scalar_one()
        ltree_id = Ltree(str(_id))
        path = ltree_id if parent is None else parent.path + ltree_id
        parent_id = None if parent is None else parent.id
        new_department = cls(
            id=_id,
            name=name,
            company_id=company_id,
            path=path,
            parent_id=parent_id,
        )
        async_session.add(new_department)
        return new_department

    def to_pydantic_schema(self) -> DepartmentSchema:
        return DepartmentSchema(**self.__dict__)
