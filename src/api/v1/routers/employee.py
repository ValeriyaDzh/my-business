from fastapi import APIRouter, Depends, Form, status

from src.api.v1.dependencies import is_admin, valid_employee
from src.api.v1.services import EmployeeService
from src.models import User
from src.schemas.employee import (
    CreateEmployee,
    EmployeeMessageCreateResponse,
    EmployeeMessageResponse,
    UpdateEmployee,
)

router = APIRouter()


@router.post(
    "/employees/create",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeMessageCreateResponse,
)
async def create_employee(
    data: CreateEmployee,
    user: User = Depends(is_admin),
    employee_service: EmployeeService = Depends(EmployeeService),
) -> None:
    message = await employee_service.create_and_send_invite(
        data,
        user.company_id,
    )

    return EmployeeMessageCreateResponse(playload=message)


@router.post(
    "/employees/registration/{token}",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeMessageResponse,
)
async def registration_employee(
    token: str,
    password: str = Form(...),
    employee_service: EmployeeService = Depends(EmployeeService),
) -> None:
    message = await employee_service.registration(password, token)
    return EmployeeMessageResponse(playload=message)


@router.patch(
    "/employees/{employee_id}/update",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeMessageResponse,
)
async def update_employee(
    update_data: UpdateEmployee,
    employee: User = Depends(valid_employee),
    employee_service: EmployeeService = Depends(EmployeeService),
) -> None:
    message = await employee_service.update(employee.id, update_data)
    return EmployeeMessageResponse(playload=message)


@router.post(
    "/employees/{employee_id}/change-email",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeMessageResponse,
)
async def change_email(
    employee: User = Depends(valid_employee),
    new_email: str = Form(...),
    employee_service: EmployeeService = Depends(EmployeeService),
) -> None:
    message = await employee_service.send_change_email(
        employee.id,
        new_email,
    )
    return EmployeeMessageResponse(playload=message)


@router.get(
    "/employees/confirm-new-email/{token}",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeMessageResponse,
)
async def confirm_new_email(
    token: str,
    employee_service: EmployeeService = Depends(EmployeeService),
) -> None:
    message = await employee_service.change_email_confirm(token)
    return EmployeeMessageResponse(playload=message)
