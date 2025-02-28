from app.core.logging_config import logger
from app.models import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import SQLALCHEMY_DATABASE_URL


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True
)
logger.info("Async sessionmaker created")


async def init_db():
    logger.info("Initializing the database schema...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully")


async def get_db():
    logger.info("Opening async database session")
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
            logger.info("Database session closed")


