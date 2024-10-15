__all__ = [
    "router_v1",
]

from fastapi import APIRouter
from src.api.v1.routers.signup import router as signup_router_v1

router_v1 = APIRouter()
router_v1.include_router(signup_router_v1, prefix="/auth/api/v1", tags=["SignUP | v1"])
