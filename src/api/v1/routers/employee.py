from fastapi import APIRouter, Depends, Form, status

from src.api.v1.dependencies import is_admin
from src.api.v1.services import EmployeeService
from src.models import User
from src.schemas.employee import (
    CreateEmployee,
    EmploeeMessageCreateResponse,
    EmploeeMessageResponse,
    UpdateEmployee,
)

router = APIRouter()


@router.post(
    "/employees/create",
    status_code=status.HTTP_201_CREATED,
    response_model=EmploeeMessageCreateResponse,
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

    return EmploeeMessageCreateResponse(playload=message)


@router.post(
    "/employees/registration/{token}",
    status_code=status.HTTP_200_OK,
    response_model=EmploeeMessageResponse,
)
async def registration_employee(
    token: str,
    password: str = Form(...),
    employee_service: EmployeeService = Depends(EmployeeService),
) -> None:
    message = await employee_service.registration(password, token)
    return EmploeeMessageResponse(playload=message)


@router.patch(
    "/employees/{employee_id}/update",
    status_code=status.HTTP_200_OK,
    response_model=EmploeeMessageResponse,
)
async def update_employee(
    employee_id: str,
    update_data: UpdateEmployee,
    user: User = Depends(is_admin),
    employee_service: EmployeeService = Depends(EmployeeService),
) -> None:
    message = await employee_service.update(employee_id, update_data)
    return EmploeeMessageResponse(playload=message)


@router.post(
    "/employees/{employee_id}/change-email",
    status_code=status.HTTP_200_OK,
    response_model=EmploeeMessageResponse,
)
async def change_email(
    employee_id: str,
    user: User = Depends(is_admin),
    new_email: str = Form(...),
    employee_service: EmployeeService = Depends(EmployeeService),
) -> None:
    message = await employee_service.send_change_email(
        employee_id,
        new_email,
    )
    return EmploeeMessageResponse(playload=message)


@router.get(
    "/employees/confirm-new-email/{token}",
    status_code=status.HTTP_200_OK,
    response_model=EmploeeMessageResponse,
)
async def confirm_new_email(
    token: str,
    employee_service: EmployeeService = Depends(EmployeeService),
) -> None:
    message = await employee_service.change_email_confirm(token)
    return EmploeeMessageResponse(playload=message)
