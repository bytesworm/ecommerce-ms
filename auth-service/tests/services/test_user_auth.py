from unittest.mock import AsyncMock
from uuid import uuid4
from fastapi import HTTPException
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_auth import UserAuth
from app.repositories.user_auth import UserAuthRepository
from app.schemas.user_auth import UserAuthCreate, UserAuthRead
from app.services.user_auth import UserAuthService


@pytest.mark.asyncio
async def test_save_success(test_session: AsyncSession) -> None:
    mock_repository = AsyncMock(spec=UserAuthRepository)
    service = UserAuthService(mock_repository)

    email = f"{uuid4()}@example.com"
    password = str(uuid4())

    user_auth_create = UserAuthCreate(email=email, password=password)
    expected_user_auth = UserAuth(id=1, email=email, password=password)

    mock_repository.get_by_email.return_value = None
    mock_repository.save.return_value = expected_user_auth

    result = await service.save(test_session, user_auth_create)

    assert isinstance(result, UserAuthRead)
    assert result.email == email
    mock_repository.get_by_email.assert_called_once()
    mock_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_save_exists(test_session: AsyncSession) -> None:
    mock_repository = AsyncMock(spec=UserAuthRepository)
    service = UserAuthService(mock_repository)

    email = f"{uuid4()}@example.com"
    password = str(uuid4())

    user_auth_create = UserAuthCreate(email=email, password=password)
    existing_user = UserAuth(id=1, email=email, password=password)

    mock_repository.get_by_email.return_value = existing_user

    with pytest.raises(HTTPException) as exc:
        await service.save(test_session, user_auth_create)

    assert exc.value.status_code == 409
    mock_repository.get_by_email.assert_called_once()
    mock_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_get_by_id_success(test_session: AsyncSession) -> None:
    mock_repository = AsyncMock(spec=UserAuthRepository)
    service = UserAuthService(mock_repository)

    user_id = 1
    email = f"{uuid4()}@example.com"
    password = str(uuid4())

    existing_user = UserAuth(id=user_id, email=email, password=password)
    mock_repository.get_by_id.return_value = existing_user

    result = await service.get_by_id(test_session, user_id)

    assert isinstance(result, UserAuthRead)
    assert result.email == email
    mock_repository.get_by_id.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id_not_found(test_session: AsyncSession) -> None:
    mock_repository = AsyncMock(spec=UserAuthRepository)
    service = UserAuthService(mock_repository)

    user_id = 1

    mock_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await service.get_by_id(test_session, user_id)

    assert exc.value.status_code == 404
    mock_repository.get_by_id.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_email_success(test_session: AsyncSession) -> None:
    mock_repository = AsyncMock(spec=UserAuthRepository)
    service = UserAuthService(mock_repository)

    email = f"{uuid4()}@example.com"
    password = str(uuid4())

    existing_user = UserAuth(id=1, email=email, password=password)
    mock_repository.get_by_email.return_value = existing_user

    result = await service.get_by_email(test_session, email)

    assert isinstance(result, UserAuthRead)
    assert result.email == email
    mock_repository.get_by_email.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_email_not_found(test_session: AsyncSession) -> None:
    mock_repository = AsyncMock(spec=UserAuthRepository)
    service = UserAuthService(mock_repository)

    email = f"{uuid4()}@example.com"

    mock_repository.get_by_email.return_value = None

    with pytest.raises(HTTPException) as exc:
        await service.get_by_email(test_session, email)

    assert exc.value.status_code == 404
    mock_repository.get_by_email.assert_called_once()
