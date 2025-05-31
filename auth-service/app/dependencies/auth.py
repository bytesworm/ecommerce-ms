from typing import Annotated

from fastapi import Depends

from app.dependencies.token import get_token_service
from app.repositories.user_auth import UserAuthRepository
from app.services.auth import AuthService
from app.services.token import TokenService


def get_auth_service(
    token_service: Annotated[TokenService, Depends(get_token_service)],
    user_auth_repo: Annotated[UserAuthRepository, Depends(UserAuthRepository)],
) -> AuthService:
    return AuthService(token_service, user_auth_repo)
