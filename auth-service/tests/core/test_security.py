from uuid import uuid4

from app.core.security import hash_password, verify_hash


def test_password_hashing() -> None:
    raw_password = str(uuid4())
    hashed_password = hash_password(raw_password)
    assert verify_hash(raw_password, hashed_password)
