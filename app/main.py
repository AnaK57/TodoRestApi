from app.core.logging_config import logger
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.api.auth import auth_router
from app.api.task import task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started...")
    await init_db()
    yield
    logger.info("Aplication finished...")


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(task_router)






