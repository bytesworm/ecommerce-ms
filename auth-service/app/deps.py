from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import AsyncSessionLocal
from app.services.auth import AuthService
from app.services.token import TokenService
from app.core.config import settings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

def get_token_service() -> TokenService:
    return TokenService(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

def get_auth_service(token_service: Annotated[TokenService, Depends(get_token_service)]) -> AuthService:
    return AuthService(token_service)
