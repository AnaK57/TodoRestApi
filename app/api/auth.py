from app.core.logging_config import logger
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth import create_access_token
from app.crud.user import get_user_by_username
from datetime import timedelta
from app.utils import verify_password
from app.crud import user
from app import schemas
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES


auth_router = APIRouter()


@auth_router.post("/auth/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    logger.info(f"Login attempt for username: {form_data.username}")
    existing_user = await get_user_by_username(db, form_data.username)
    if not existing_user or not verify_password(form_data.password, existing_user.hashed_password):
        logger.warning(f"Login failed for username: {form_data.username}")
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": existing_user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    logger.info(f"Login successful for username: {existing_user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: schemas.User, db: AsyncSession = Depends(get_db)):
    logger.info(f"Registration attempt for username: {user_data.username}")
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        logger.warning(f"Registration failed: username {user_data.username} already exists")
        raise HTTPException(status_code=400, detail="Username already exists")

    await user.create_user(db, user_data.username, user_data.password)
    logger.info(f"User {user_data.username} registered successfully")
    return {"message": "User registered successfully!"}