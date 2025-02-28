import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock

# Helper Functions
def create_mock_result_for_scalar_one_or_none(value):
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none = lambda: value
    return mock_result


def create_mock_result_for_scalars(all_return_value):
    mock_scalars = AsyncMock()
    mock_scalars.all = AsyncMock(return_value=all_return_value)
    mock_result = AsyncMock()
    # Use a lambda to ensure immediate return of mock_scalars
    mock_result.scalars = lambda: mock_scalars
    return mock_result


# Fixture for the Mocked DB Session
@pytest.fixture
def mock_db():
    db = AsyncMock(spec=AsyncSession)
    db.add = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.delete = AsyncMock()
    db.execute = AsyncMock()
    return db