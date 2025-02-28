import pytest
from app.crud.user import get_user_by_username, create_user
from app.models.user import User
from tests.unit.conftest import create_mock_result_for_scalar_one_or_none
from fastapi import HTTPException


@pytest.mark.asyncio
class TestUserCRUD:

    async def test_get_user_by_username(self, mock_db):
        expected_user = User(id=1, username="testuser", hashed_password="hashed_secret")
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(expected_user)

        user_found = await get_user_by_username(mock_db, "testuser")

        assert user_found is not None
        assert user_found.id == 1
        assert user_found.username == "testuser"
        mock_db.execute.assert_called_once()


    async def test_get_user_by_username_incorrect_password(self, mock_db):
        expected_user = User(id=1, username="testuser", hashed_password="")
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(expected_user)

        user_found = await get_user_by_username(mock_db, "testuser")

        assert user_found is not None
        assert user_found.id == 1
        assert user_found.username == "testuser"
        mock_db.execute.assert_called_once()


    async def test_get_user_by_username_not_found(self, mock_db):
        username = "nonexistentuser"
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(None)

        user_found = await get_user_by_username(mock_db, username)

        assert user_found is None
        mock_db.execute.assert_called_once()


    async def test_get_user_by_username_db_error(self, mock_db):
        # Simuliramo da baza baci Exception prilikom izvršavanja upita
        mock_db.execute.side_effect = Exception("Database failure")

        with pytest.raises(HTTPException) as exc_info:
            await get_user_by_username(mock_db, "testuser")

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Database error"
        mock_db.execute.assert_called_once()

    async def test_create_user(self, mock_db, monkeypatch):
        # Simuliraj da korisnik ne postoji u bazi
        mock_db.execute.return_value = create_mock_result_for_scalar_one_or_none(None)

        # Monkeypatch za hash_password kako bi imao predvidljiv hash
        monkeypatch.setattr("app.crud.user.hash_password", lambda pwd: f"hashed_{pwd}")

        username = "newuser"
        password = "secret"
        created_user = await create_user(mock_db, username, password)

        # Provjera da su vrijednosti ispravne
        assert created_user.username == username
        assert created_user.hashed_password == f"hashed_{password}"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


