from fastapi import APIRouter, Depends, Form, Request, status

from src.api.v1.dependencies import is_admin
from src.api.v1.services import DepartmentService
from src.models import User
from src.schemas.department import (
    DepartmentCreateResponse,
    DepartmentListResponse,
    DepartmentResponse,
    DepartmentUpdateRequest,
)

router = APIRouter()


@router.post(
    "/departments",
    status_code=status.HTTP_201_CREATED,
    response_model=DepartmentCreateResponse,
)
async def create_departments(
    user: User = Depends(is_admin),
    name_department: str = Form(...),
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    department = await department_service.create(
        user.company_id,
        name_department,
    )
    return DepartmentCreateResponse(playload=department)


@router.get(
    "/departments",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentListResponse,
)
async def get_departments(
    request: Request,
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    departments = await department_service.get_all(request.state.user.company_id)
    return DepartmentListResponse(payload=departments)


@router.post(
    "/departments/department/{department_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=DepartmentCreateResponse,
)
async def create_department(
    department_id: int,
    name_department: str = Form(...),
    user: User = Depends(is_admin),
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    department = await department_service.create(
        user.company_id,
        name_department,
        department_id,
    )
    return DepartmentCreateResponse(payload=department)


@router.get(
    "/departments/department/{department_id}",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentListResponse,
)
async def get_subdepartments(
    request: Request,
    department_id: int,
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    departments = await department_service.get_subdepartments(
        request.state.user.company_id,
        department_id,
    )
    return DepartmentListResponse(payload=departments)


@router.patch(
    "/departments/department/{department_id}",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentResponse,
)
async def update_department(
    department_id: int,
    department_data: DepartmentUpdateRequest,
    user: User = Depends(is_admin),
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    department = await department_service.update(
        user.company_id,
        department_id,
        department_data,
    )
    return DepartmentResponse(payload=department)


@router.delete(
    "/departments/department/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_department(
    department_id: int,
    user: User = Depends(is_admin),
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    return await department_service.delete(
        user.company_id,
        department_id,
    )
