from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.utils.custom_types import uuid_pk


class Company(Base):

    __tablename__ = "company"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String, unique=True)
