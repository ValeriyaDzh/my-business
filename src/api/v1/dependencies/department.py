import logging

from fastapi import Depends

from src.api.v1.dependencies.admin import is_admin
from src.api.v1.services import DepartmentService
from src.models import Department, User
from src.utils.exceptions import NotFoundException

logger = logging.getLogger(__name__)


async def valid_department(
    department_id: int,
    admin: User = Depends(is_admin),
    department_service: DepartmentService = Depends(DepartmentService),
) -> DepartmentService:
    department: Department = await department_service.get_by_id(department_id)
    if not department or department.company_id != admin.company_id:
        raise NotFoundException("Department not found")
    return department
