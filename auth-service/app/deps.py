from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import AsyncSessionLocal
from app.schemes.user_auth import UserAuthRead
from app.services.auth import AuthService
from app.services.token import TokenService
from app.core.config import settings
from app.services.user_auth import UserAuthService


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserAuthRead:
    token_data = token_service.decode(token)
    user = await user_auth_service.get_by_email(db, token_data.sub)
    return user
