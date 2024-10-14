from typing import Annotated
from uuid import uuid4

from sqlalchemy import UUID
from sqlalchemy.orm import mapped_column


uuid_pk = Annotated[
    UUID,
    mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    ),
]
