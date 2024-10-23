from fastapi import APIRouter, Depends, Form, Request, status

from src.api.v1.services import EmployeeService
from src.schemas.base import Message
from src.schemas.employee import CreateEmployee, UpdateEmployee

router = APIRouter()


@router.post(
    "/employees/create",
    status_code=status.HTTP_201_CREATED,
    response_model=Message,
)
async def create_employee(
    data: CreateEmployee,
    request: Request,
    employee_service: EmployeeService = Depends(EmployeeService),
):
    await employee_service.create_and_send_invite(
        data,
        request.state.is_admin,
        request.state.company_id,
    )

    return Message(message="Invite mail has been sent")


@router.post(
    "/employees/registration/{token}",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
async def registration_employee(
    token: str,
    password: str = Form(...),
    employee_service: EmployeeService = Depends(EmployeeService),
):
    await employee_service.registration(password, token)
    return Message(message="Done...")


@router.patch(
    "/employees/{employee_id}/update",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
async def update_employee(
    employee_id: str,
    update_data: UpdateEmployee,
    request: Request,
    employee_service: EmployeeService = Depends(EmployeeService),
):
    await employee_service.update(employee_id, request.state.is_admin, update_data)
    return Message(message="Done...")


@router.post(
    "/employees/{employee_id}/change-email",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
async def change_email(
    employee_id: str,
    request: Request,
    new_email: str = Form(...),
    employee_service: EmployeeService = Depends(EmployeeService),
):
    await employee_service.send_change_email(
        employee_id, request.state.is_admin, new_email
    )
    return Message(message="Email has been sent")


@router.get(
    "/employees/confirm-new-email/{token}",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
async def confirm_new_email(
    token: str,
    employee_service: EmployeeService = Depends(EmployeeService),
):
    await employee_service.change_email_confirm(token)
    return Message(message="New mail has been successfully confirmed")
