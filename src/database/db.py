import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

logger = logging.getLogger(__name__)

async_engine = create_async_engine(url=settings.db.URL.get_secret_value())

async_session_maker = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session_maker() as session:
            yield session
    except OSError as e:
        logger.error(f"Database connection failed: {e}")
