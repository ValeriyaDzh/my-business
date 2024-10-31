import logging

from fastapi import Request
from src.models import User
from src.utils.exceptions import ForbiddenException

logger = logging.getLogger(__name__)


async def is_admin(request: Request) -> User:
    logger.debug(f"Eeeeeyyy: {request.state.user}")
    if not request.state.user.is_admin:
        raise ForbiddenException("Don't have enough rights to make changes")
    return request.state.user
