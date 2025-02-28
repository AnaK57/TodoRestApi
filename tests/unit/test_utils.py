
from app.utils import hash_password, verify_password


def test_hash_password():
    password = "securepassword"
    hashed = hash_password(password)
    assert hashed != password
    assert isinstance(hashed, str)
    assert verify_password(password, hashed)


def test_verify_password():
    password = "mypassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_empty_password():
    password = ""
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)

