from uuid import uuid4
from httpx import AsyncClient, ASGITransport
import pytest
from app.main import app
from app.schemas.auth import AuthRequest
from app.schemas.user_auth import UserAuthCreate, UserAuthRead


@pytest.mark.asyncio
async def test_get_user_auth_not_found() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        id = -1
        response = await ac.get(f"/user-auth?id={id}")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_auth_success() -> None:
    email = f"{uuid4()}@example.com"
    test_user = UserAuthCreate(email=email, password=str(uuid4()))

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response_1 = await ac.post("/user-auth", json=test_user.model_dump())
        data = response_1.json()
        user_id = data["id"]
        response = await ac.get(f"/user-auth?id={user_id}")
        expected_data = UserAuthRead(id=user_id, email=email)

        assert response.status_code == 200
        assert response.json() == expected_data.model_dump()


@pytest.mark.asyncio
async def test_create_user_auth_success() -> None:
    test_user = UserAuthCreate(email=f"{uuid4()}@example.com", password=str(uuid4()))

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/user-auth", json=test_user.model_dump())
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user_auth_exists() -> None:
    test_user = UserAuthCreate(email=f"{uuid4()}@example.com", password=str(uuid4()))

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post("/user-auth", json=test_user.model_dump())
        response = await ac.post("/user-auth", json=test_user.model_dump())

        assert response.status_code == 409


@pytest.mark.asyncio
async def test_auth_and_get_me() -> None:
    email = f"{uuid4()}@example.com"
    password = str(uuid4())
    test_user = UserAuthCreate(email=email, password=password)
    auth_request = AuthRequest(email=email, password=password)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        user_res = await ac.post("/user-auth", json=test_user.model_dump())
        user_data = user_res.json()
        expected_user = UserAuthRead(id=user_data["id"], email=email)

        auth_res = await ac.post("/login", json=auth_request.model_dump())
        auth_data = auth_res.json()
        token, token_type = auth_data["access_token"], auth_data["token_type"]
        headers = {"Authorization": f"{token_type} {token}"}

        response = await ac.get("/user-auth/me", headers=headers)
        assert response.status_code == 200
        assert response.json() == expected_user.model_dump()
