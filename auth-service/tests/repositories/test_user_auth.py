from uuid import uuid4
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user_auth import UserAuth
from app.repositories.user_repository import UserAuthRepository


@pytest.fixture
def repository() -> UserAuthRepository:
    return UserAuthRepository()


@pytest.mark.asyncio
async def test_save_success(test_session: AsyncSession, repository: UserAuthRepository) -> None:
    test_email = f"{uuid4()}@example.com"
    password = str(uuid4())
    hashed_password = hash_password(password)

    user_auth = UserAuth(email=test_email, password=hashed_password)
    await repository.save(test_session, user_auth)

    assert user_auth.id is not None


@pytest.mark.asyncio
async def test_save_unique_fail(test_session: AsyncSession, repository: UserAuthRepository) -> None:
    test_email = f"{uuid4()}@example.com"
    password = str(uuid4())
    hashed_password = hash_password(password)

    user_auth = UserAuth(email=test_email, password=hashed_password)
    user_auth_second = UserAuth(email=test_email, password=hashed_password)
    await repository.save(test_session, user_auth)

    with pytest.raises(IntegrityError):
        await repository.save(test_session, user_auth_second)


@pytest.mark.asyncio
async def test_save_nullable_fail(test_session: AsyncSession, repository: UserAuthRepository) -> None:
    test_email = None
    password = None

    user_auth = UserAuth(email=test_email, password=password)

    with pytest.raises(IntegrityError):
        await repository.save(test_session, user_auth)


@pytest.mark.asyncio
async def test_get_by_id_success(
    test_session: AsyncSession, repository: UserAuthRepository
) -> None:
    test_email = f"{uuid4()}@example.com"
    password = str(uuid4())
    hashed_password = hash_password(password)

    user_auth = UserAuth(email=test_email, password=hashed_password)
    await repository.save(test_session, user_auth)

    user_from_db = await repository.get_by_id(test_session, user_auth.id)

    assert user_from_db is not None
    assert user_from_db.id == user_auth.id


@pytest.mark.asyncio
async def test_get_by_id_none_success(
    test_session: AsyncSession, repository: UserAuthRepository
) -> None:
    user_from_db = await repository.get_by_id(test_session, -1)

    assert user_from_db is None

@pytest.mark.asyncio
async def test_get_by_email_success(
    test_session: AsyncSession, repository: UserAuthRepository
) -> None:
    test_email = f"{uuid4()}@example.com"
    password = str(uuid4())
    hashed_password = hash_password(password)

    user_auth = UserAuth(email=test_email, password=hashed_password)
    await repository.save(test_session, user_auth)

    user_from_db = await repository.get_by_email(test_session, user_auth.email)

    assert user_from_db is not None
    assert user_from_db.email == user_auth.email


@pytest.mark.asyncio
async def test_get_by_email_none_success(
    test_session: AsyncSession, repository: UserAuthRepository
) -> None:
    test_email = f"{uuid4()}@none.com"

    user_from_db = await repository.get_by_email(test_session, test_email)

    assert user_from_db is None
