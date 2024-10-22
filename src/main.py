import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1 import router_v1

from src.middlware.auth import AuthMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.info("Starting app...")
    yield


app = FastAPI(title="MyBusiness", lifespan=lifespan)
app.include_router(router_v1)

exclude_paths = [
    "/openapi.json",
    "/docs",
    "/redoc",
    "/auth/api/v1/sign-in",
    "/auth/api/v1/check_account",
    "/auth/api/v1/sign-up",
    "/auth/api/v1/sign-up-complete",
]

app.add_middleware(AuthMiddleware, exclude_paths=exclude_paths)
