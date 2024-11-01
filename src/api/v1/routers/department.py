from fastapi import APIRouter, Depends, Form, Request, status

from src.api.v1.services import DepartmentService
from src.schemas.department import Department, DepartmentUpdate

router = APIRouter()


@router.post(
    "/departments",
    status_code=status.HTTP_201_CREATED,
    response_model=Department,
)
async def create_departments(
    request: Request,
    name_department: str = Form(...),
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    return await department_service.create(
        request.state.company_id,
        request.state.is_admin,
        name_department,
    )


@router.get(
    "/departments",
    status_code=status.HTTP_200_OK,
    response_model=list[Department],
)
async def get_departments(
    request: Request,
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
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
) -> None:
    return await department_service.create(
        request.state.company_id,
        request.state.is_admin,
        name_department,
        department_id,
    )


@router.get(
    "/departments/department/{department_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[Department],
)
async def get_subdepartments(
    request: Request,
    department_id: int,
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    return await department_service.get_subdepartments(
        request.state.company_id,
        request.state.is_admin,
        department_id,
    )


@router.patch(
    "/departments/department/{department_id}",
    status_code=status.HTTP_200_OK,
    response_model=Department,
)
async def update_department(
    request: Request,
    department_id: int,
    department_data: DepartmentUpdate,
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    return await department_service.update(
        request.state.company_id,
        request.state.is_admin,
        department_id,
        department_data,
    )


@router.delete(
    "/departments/department/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_department(
    request: Request,
    department_id: int,
    department_service: DepartmentService = Depends(DepartmentService),
) -> None:
    return await department_service.delete(
        request.state.company_id,
        request.state.is_admin,
        department_id,
    )
