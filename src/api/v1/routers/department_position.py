from fastapi import APIRouter, Depends, status

from src.api.v1.dependencies import valid_department, valid_position
from src.api.v1.services import DepartmentPositionService
from src.models import Department, Position
from src.schemas.base import BaseMessageResponse
from src.schemas.position import PositionListResponse

router = APIRouter()


@router.get(
    "/departments/{department_id}/positions",
    status_code=status.HTTP_200_OK,
    response_model=PositionListResponse,
)
async def get_positions_from_department(
    department: Department = Depends(valid_department),
    department_position_service: DepartmentPositionService = Depends(
        DepartmentPositionService
    ),
) -> None:
    positions = await department_position_service.get_positions(department)
    return PositionListResponse(playload=positions)


@router.post(
    "/departments/{department_id}/positions/{position_id}",
    status_code=status.HTTP_200_OK,
    response_model=BaseMessageResponse,
)
async def add_position_to_department(
    position: Position = Depends(valid_position),
    department: Department = Depends(valid_department),
    department_position_service: DepartmentPositionService = Depends(
        DepartmentPositionService
    ),
) -> None:
    message = await department_position_service.add_position(department, position)
    return BaseMessageResponse(playload=message)


@router.delete(
    "/departments/{department_id}/positions/{position_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_position_from_department(
    position: Position = Depends(valid_position),
    department: Department = Depends(valid_department),
    department_position_service: DepartmentPositionService = Depends(
        DepartmentPositionService
    ),
) -> None:
    await department_position_service.remove_position(department.id, position.id)
