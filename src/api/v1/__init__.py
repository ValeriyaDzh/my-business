__all__ = [
    "router_v1",
]

from fastapi import APIRouter

from src.api.v1.routers.department import router as department_router_v1
from src.api.v1.routers.department_position import router as dep_pos_router_v1
from src.api.v1.routers.employee import router as employee_router_v1
from src.api.v1.routers.employee_position import router as emp_pos_router_v1
from src.api.v1.routers.position import router as position_router_v1
from src.api.v1.routers.signin import router as signin_router_v1
from src.api.v1.routers.signup import router as signup_router_v1
from src.api.v1.routers.task import router as task_router_v1

router_v1 = APIRouter()
router_v1.include_router(
    dep_pos_router_v1,
    prefix="/api/v1",
    tags=["Department-Position | v1"],
)
router_v1.include_router(
    department_router_v1,
    prefix="/api/v1",
    tags=["Department | v1"],
)
router_v1.include_router(
    emp_pos_router_v1,
    prefix="/api/v1",
    tags=["Employee-Position | v1"],
)
router_v1.include_router(employee_router_v1, prefix="/api/v1", tags=["Employee | v1"])
router_v1.include_router(position_router_v1, prefix="/api/v1", tags=["Position | v1"])
router_v1.include_router(signin_router_v1, prefix="/auth/api/v1", tags=["Sign-in | v1"])
router_v1.include_router(signup_router_v1, prefix="/auth/api/v1", tags=["Sign-up | v1"])
router_v1.include_router(task_router_v1, prefix="/api/v1", tags=["Task | v1"])
