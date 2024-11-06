from uuid import UUID

from fastapi import Depends

from src.api.v1.dependencies.admin import is_admin
from src.api.v1.services import UserService
from src.models import User
from src.utils.exceptions import NotFoundException


async def valid_employee(
    employee_id: UUID,
    admin: User = Depends(is_admin),
    user_service: UserService = Depends(UserService),
) -> User:
    employee: User = await user_service.get_by_id(employee_id)
    if not employee or employee.company_id != admin.company_id:
        raise NotFoundException("Employee not found")
    return employee
