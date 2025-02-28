import pytest
import jwt
from datetime import timedelta, datetime
from fastapi import HTTPException
from app.core.auth import (
    create_access_token,
    verify_token,
    get_current_user,
    SECRET_KEY,
    ALGORITHM
)
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    assert isinstance(token, str)

    # Decode the token to verify the data
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_verify_token_valid():
    data = {"sub": "validuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))

    username = verify_token(token, HTTPException(status_code=401, detail="Invalid token"))
    assert username == "validuser"


@pytest.mark.asyncio
async def test_verify_token_invalid():
    invalid_token = "invalid.token.value"

    with pytest.raises(HTTPException) as excinfo:
        verify_token(invalid_token, HTTPException(status_code=401, detail="Invalid token"))

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid token"


@pytest.mark.asyncio
async def test_verify_token_expired():
    expired_data = {"sub": "expireduser", "exp": datetime.utcnow() - timedelta(minutes=1)}
    expired_token = jwt.encode(expired_data, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        verify_token(expired_token, HTTPException(status_code=401, detail="Invalid token"))

    assert excinfo.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(mocker):
    fake_user = {"username": "testuser"}
    mocker.patch("app.core.auth.get_user_by_username", new=AsyncMock(return_value=fake_user))

    mock_db = AsyncMock()
    token = create_access_token({"sub": "testuser"})
    user = await get_current_user(token, mock_db)

    assert user["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_current_user_not_found(mocker):
    mocker.patch("app.core.auth.get_user_by_username", new=AsyncMock(return_value=None))

    mock_db = AsyncMock()
    token = create_access_token({"sub": "nonexistentuser"})

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token, mock_db)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid authentication credentials"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    invalid_token = "invalid.token.value"
    mock_db = AsyncMock()

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(invalid_token, mock_db)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid authentication credentials"
