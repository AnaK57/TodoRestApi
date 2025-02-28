import pytest
from pydantic import ValidationError
from app.crud import task
from app.models.task import Task, TaskStatus
from app.schemas import TaskCreate, TaskUpdate
from tests.unit.conftest import create_mock_result_for_scalar_one_or_none
from tests.unit.conftest import create_mock_result_for_scalars
from fastapi import HTTPException


@pytest.mark.asyncio
class TestTaskCRUD:

    async def test_create_task(self, mock_db):
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            status=TaskStatus.open
        )
        created_task = await task.create_task(mock_db, task_data)

        assert created_task.title == task_data.title
        assert created_task.description == task_data.description
        assert created_task.status == task_data.status

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


    async def test_create_task_short_title(mock_db):
        with pytest.raises(ValidationError) as exc_info:
            task_data = TaskCreate(
                title="ab",
                description="Valid description",
                status=TaskStatus.open
            )

        assert "String should have at least 3 characters" in str(exc_info.value)


    async def test_create_task_invalid_status(mock_db):
        with pytest.raises(ValidationError) as exc_info:
            task_data = TaskCreate(
                title="Valid Title",
                description="Valid Description",
                status="invalid_status"
            )

        assert "Input should be 'open', 'in-progress' or 'closed" in str(exc_info.value)


    async def test_create_task_db_error(self, mock_db, monkeypatch):
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            status=TaskStatus.open
        )
        mock_db.commit.side_effect = Exception("Database failure")
        with pytest.raises(HTTPException) as exc_info:
            await task.create_task(mock_db, task_data)
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Database error"
        mock_db.rollback.assert_called_once()


    async def test_get_tasks(self, mock_db):
        mock_db.execute.return_value = create_mock_result_for_scalars(
            [Task(id=1, title="Task 1", status=TaskStatus.open)]
        )
        # First await returns a coroutine (from .all())
        tasks_coro = await task.get_tasks(mock_db)
        # Second await resolves the coroutine
        tasks = await tasks_coro

        assert len(tasks) == 1
        assert tasks[0].title == "Task 1"
        mock_db.execute.assert_called_once()


    async def test_get_task(self, mock_db):
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(
            Task(id=1, title="Task 1", status=TaskStatus.open)
        )
        fetched_task = await task.get_task(mock_db, 1)

        assert fetched_task is not None
        assert fetched_task.id == 1
        assert fetched_task.title == "Task 1"
        mock_db.execute.assert_called_once()


    async def test_get_task_not_found(self, mock_db):
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(None)

        fetched_task = await task.get_task(mock_db, 999)

        assert fetched_task is None
        mock_db.execute.assert_called_once()


    async def test_update_task(self, mock_db):
        existing_task = Task(id=1, title="Old Title", description="Old Description", status=TaskStatus.open)
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(existing_task)

        update_data = TaskUpdate(
            title="Updated Task",
            description="Updated Description",
            status=TaskStatus.in_progress
        )
        updated_task = await task.update_task(mock_db, 1, update_data)

        assert updated_task.title == update_data.title
        assert updated_task.description == update_data.description
        assert updated_task.status == update_data.status
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


    async def test_update_task_not_found(self, mock_db):
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(None)

        update_data = TaskUpdate(
            title="Updated Task",
            description="Updated Description",
            status=TaskStatus.in_progress
        )
        updated_task = await task.update_task(mock_db, 999, update_data)

        assert updated_task is None
        mock_db.execute.assert_called_once()


    async def test_delete_task(self, mock_db):
        existing_task = Task(id=1, title="Task to Delete", description="Description", status=TaskStatus.open)
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(existing_task)

        deleted_task = await task.delete_task(mock_db, 1)
        assert deleted_task.id == 1
        mock_db.delete.assert_called_once_with(existing_task)
        mock_db.commit.assert_called_once()


    async def test_delete_task_not_found(self, mock_db):
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(None)

        deleted_task = await task.delete_task(mock_db, 999)

        assert deleted_task is None
        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()