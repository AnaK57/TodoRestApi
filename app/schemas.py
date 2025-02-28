from pydantic import BaseModel, Field
from datetime import datetime
from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Title must be between 3 and 255 characters."
    )
    description: str | None = Field(
        None,
        max_length=1000,
        description="The maximum length of the description is 1000 characters."
    )
    status: TaskStatus = Field(
        ...,
        description="Allowed statuses are: open, in_progress, closed."
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username must be between 3 and 50 characters."
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Password must be at least 6 characters long."
    )