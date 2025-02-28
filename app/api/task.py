from app.core.logging_config import logger
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import schemas
from app.crud import task
from app.core.auth import get_current_user
from app.config import TASKS_FETCH_LIMIT


task_router = APIRouter()


def handle_task_not_found(task_id: int):
    logger.error(f"Task with ID={task_id} not found")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found"
    )


@task_router.get("/tasks", response_model=list[schemas.TaskResponse])
async def get_all_tasks(skip: int = 0, limit: int = TASKS_FETCH_LIMIT, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.info(f"Fetching tasks with skip={skip} and limit={limit}, current user is {current_user.username}")
    tasks = await task.get_tasks(db, skip=skip, limit=limit)
    logger.info(f"Found {len(tasks)} tasks")
    return tasks


@task_router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.info(f"Fetching tasks with ID={task_id}, current user is {current_user.username}")
    task_one = await task.get_task(db, task_id)
    if task_one is None:
        handle_task_not_found(task_id)
    logger.info(f"Task with ID={task_id} found")
    return task_one


@task_router.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(new_task: schemas.TaskCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.info(f"Creating new task with title={new_task.title}, current user is {current_user.username}")
    return await task.create_task(db, new_task)


@task_router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(task_id: int, new_task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.info(f"Updating task with ID={task_id}, current user is {current_user.username}")
    db_task = await task.update_task(db=db, task_id=task_id, new_task=new_task)
    if db_task is None:
        handle_task_not_found(task_id)
    logger.info(f"Updated task with ID={task_id}")
    return db_task


@task_router.delete("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.info(f"Deleting task with ID={task_id}, current user is {current_user.username}")
    db_task = await task.delete_task(db=db, task_id=task_id)
    if db_task is None:
        handle_task_not_found(task_id)
    logger.info(f"Deleted task with ID={task_id}")
    return db_task



