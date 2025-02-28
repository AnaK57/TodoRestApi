from app.core.logging_config import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task
from app import schemas
from fastapi import HTTPException


async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching tasks with skip={skip} and limit={limit}")
    result = await db.execute(select(Task).offset(skip).limit(limit))
    return result.scalars().all()


async def get_task(db: AsyncSession, task_id: int):
    logger.info(f"Fetching task with ID={task_id}")
    try:
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error fetching task: {str(e)}")
        return None


async def create_task(db: AsyncSession, new_task: schemas.TaskCreate):
    logger.info(f"Creating new task with title={new_task.title}")
    db_task = Task(**new_task.model_dump())

    db.add(db_task)
    try:
        await db.commit()
        await db.refresh(db_task)
        logger.info(f"Created task with ID={db_task.id}")
        return db_task
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")


async def update_task(db: AsyncSession, task_id: int, new_task: schemas.TaskUpdate):
    logger.info(f"Updating task with ID={task_id}")
    db_task = await get_task(db, task_id)
    if not db_task:
        logger.warning(f"Task with ID={task_id} not found")
        return None

    for key, value in new_task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    try:
        await db.commit()
        await db.refresh(db_task)
        logger.info(f"Updated task with ID={task_id}")
        return db_task
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

async def delete_task(db: AsyncSession, task_id: int):
    logger.info(f"Deleting task with ID={task_id}")
    db_task = await get_task(db, task_id)
    if not db_task:
        logger.warning(f"Task with ID={task_id} not found")
        return None

    try:
        await db.delete(db_task)
        await db.commit()
        logger.info(f"Deleted task with ID={task_id}")
        return db_task
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
