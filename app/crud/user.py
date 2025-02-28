from app.core.logging_config import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.utils import hash_password
from fastapi import HTTPException


async def get_user_by_username(db: AsyncSession, username: str):
    logger.info(f"Fetching user with username={username}")
    try:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")


async def create_user(db: AsyncSession, username: str, password: str):
    existing_user = await get_user_by_username(db, username)
    if existing_user:
        logger.warning(f"User with username={username} already exists")
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pwd = hash_password(password)
    db_user = User(username=username, hashed_password=hashed_pwd)
    db.add(db_user)

    try:
        await db.commit()
        await db.refresh(db_user)
        logger.info(f"User {username} successfully created")
        return db_user
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")