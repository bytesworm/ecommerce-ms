import pytest
from app.models.user import User
from app.repositories.user_repository import UserRepository

from faker import Faker


@pytest.mark.asyncio
async def test_create_user(db):
    faker = Faker()
    repo = UserRepository()
    username = faker.user_name()
    password = faker.password()
    user = User(username=username, hashed_password=password)

    result = await repo.save(db, user)

    assert result.id is not None
    assert result.username == username
