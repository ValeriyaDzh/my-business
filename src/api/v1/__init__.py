__all__ = [
    "router_v1",
]

from fastapi import APIRouter

from src.api.v1.routers.department import router as department_router_v1
from src.api.v1.routers.employee import router as employee_router_v1
from src.api.v1.routers.signin import router as signin_router_v1
from src.api.v1.routers.signup import router as signup_router_v1

router_v1 = APIRouter()
router_v1.include_router(
    department_router_v1, prefix="/api/v1", tags=["Department | v1"],
)
router_v1.include_router(employee_router_v1, prefix="/api/v1", tags=["Employee | v1"])
router_v1.include_router(signin_router_v1, prefix="/auth/api/v1", tags=["Sign-in | v1"])
router_v1.include_router(signup_router_v1, prefix="/auth/api/v1", tags=["Sign-up | v1"])
