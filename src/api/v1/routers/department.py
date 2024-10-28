from fastapi import APIRouter, Depends, Form, Request, status

from src.api.v1.services import DepartmentService
from src.schemas.department import Department

router = APIRouter()


@router.post(
    "/departments", status_code=status.HTTP_201_CREATED, response_model=Department,
)
async def create_departments(
    request: Request,
    name_department: str = Form(...),
    department_service: DepartmentService = Depends(DepartmentService),
):
    return await department_service.create(
        request.state.company_id, request.state.is_admin, name_department,
    )


@router.get(
    "/departments", status_code=status.HTTP_200_OK, response_model=list[Department],
)
async def get_departments(
    request: Request,
    department_service: DepartmentService = Depends(DepartmentService),
):
    return await department_service.get_all(request.state.company_id)


@router.post(
    "/departments/department/{department_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=Department,
)
async def create_department(
    request: Request,
    department_id: int,
    name_department: str = Form(...),
    department_service: DepartmentService = Depends(DepartmentService),
):
    return await department_service.create(
        request.state.company_id, request.state.is_admin, name_department, department_id,
    )
