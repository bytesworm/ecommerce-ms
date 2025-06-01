from typing import AsyncGenerator
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.dependencies.db import get_db
from app.models.base import Base
from app.main import app


test_engine = create_async_engine("sqlite+aiosqlite://", echo=True)
TestAsyncSessionLocal = async_sessionmaker(test_engine)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        yield session


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:  # pragma: no cover
    async with TestAsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = get_test_db
