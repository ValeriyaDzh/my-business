from fastapi import APIRouter, Depends, status

from src.api.v1.dependencies import valid_department, valid_employee
from src.api.v1.services import EmployeePositionService
from src.models import Department, Position, User
from src.schemas.employee import EmployeeBaseResponse

router = APIRouter()


@router.post(
    "/departments/{department_id}/positions/{position_id}/employees/{employee_id}",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeBaseResponse,
)
async def appoint_employee(
    department: Department = Depends(valid_department),
    position: Position = Depends(valid_department),
    employee: User = Depends(valid_employee),
    employee_position_service: EmployeePositionService = Depends(
        EmployeePositionService,
    ),
) -> None:
    employee = await employee_position_service.appoint_employee(
        department.id, position.id, employee.id,
    )
    return EmployeeBaseResponse(playload=employee)


@router.delete(
    "/departments/{department_id}/positions/{position_id}/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_employee(
    department: Department = Depends(valid_department),
    position: Position = Depends(valid_department),
    employee: User = Depends(valid_employee),
    employee_position_service: EmployeePositionService = Depends(
        EmployeePositionService,
    ),
) -> None:
    await employee_position_service.remove_position(
        department.id, position.id, employee,
    )
