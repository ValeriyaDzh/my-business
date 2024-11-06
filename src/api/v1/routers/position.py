from fastapi import APIRouter, Depends, Form, status

from src.api.v1.dependencies import is_admin, valid_position_admin
from src.api.v1.services import PositionService
from src.models import User
from src.schemas.position import (
    PositionCreateResponse,
    PositionListResponse,
    PositionResponse,
)

router = APIRouter()


@router.post(
    "/positions",
    status_code=status.HTTP_201_CREATED,
    response_model=PositionCreateResponse,
)
async def create_position(
    position_name: str = Form(...),
    user: User = Depends(is_admin),
    position_service: PositionService = Depends(PositionService),
):
    position = await position_service.create(position_name, user.company_id)
    return PositionCreateResponse(playload=position)


@router.get(
    "/positions", status_code=status.HTTP_200_OK, response_model=PositionListResponse,
)
async def get_positions(
    user: User = Depends(is_admin),
    position_service: PositionService = Depends(PositionService),
):
    positions = await position_service.get_all(user.company_id)
    return PositionListResponse(playload=positions)


@router.patch(
    "/positions/position/{position_id}",
    status_code=status.HTTP_200_OK,
    response_model=PositionResponse,
)
async def edit_position(
    position_id: int,
    new_name: str = Form(...),
    position_service: PositionService = Depends(valid_position_admin),
):
    position = await position_service.update(position_id, new_name)
    return PositionResponse(playload=position)


@router.delete(
    "/positions/position/{position_id}", status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_position(
    position_id: int,
    new_name: str = Form(...),
    position_service: PositionService = Depends(valid_position_admin),
):
    position = await position_service.update(position_id, new_name)
    return PositionResponse(playload=position)
