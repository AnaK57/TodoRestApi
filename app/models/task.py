from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from app.models import Base
import enum


class TaskStatus(str, enum.Enum):
    open = "open"
    in_progress = "in-progress"
    closed = "closed"


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(TaskStatus), default=TaskStatus.open)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}', status={self.status}')>"
