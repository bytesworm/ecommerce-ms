from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.dependencies.user_auth import get_user_auth_service
from app.schemas.user_auth import UserAuthRead
from app.services.token import TokenService
from app.core.config import settings
from app.services.user_auth import UserAuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_token_service() -> TokenService:
    return TokenService(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    user_auth_service: Annotated[UserAuthService, Depends(get_user_auth_service)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserAuthRead:
    token_data = token_service.decode(token)
    user = await user_auth_service.get_by_email(db, token_data.sub)
    return user
