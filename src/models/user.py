from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.utils.custom_types import uuid_pk


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid_pk]
    account: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[str] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE")
    )
