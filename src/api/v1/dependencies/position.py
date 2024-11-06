import logging

from fastapi import Depends

from src.api.v1.dependencies.admin import is_admin
from src.api.v1.services import PositionService
from src.models import Position, User
from src.utils.exceptions import NotFoundException

logger = logging.getLogger(__name__)


async def valid_position_admin(
    position_id: int,
    admin: User = Depends(is_admin),
    position_service: PositionService = Depends(PositionService),
) -> PositionService:
    position: Position = await position_service.get_by_id(position_id)
    logger.debug(f"Position admin check: {position.company_id=} - {admin.company_id=}")
    if not position or position.company_id != admin.company_id:
        raise NotFoundException("Position not found")
    return position_service


async def valid_position(
    position_id: int,
    admin: User = Depends(is_admin),
    position_service: PositionService = Depends(PositionService),
) -> PositionService:
    position: Position = await position_service.get_by_id(position_id)
    logger.debug(f"Position admin check: {position.company_id=} - {admin.company_id=}")
    if not position or position.company_id != admin.company_id:
        raise NotFoundException("Position not found")
    return position
