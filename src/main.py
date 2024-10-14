import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.info("Starting app...")
    yield


app = FastAPI(title="MyBusiness", lifespan=lifespan)
