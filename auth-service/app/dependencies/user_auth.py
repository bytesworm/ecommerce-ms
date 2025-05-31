from typing import Annotated
from fastapi import Depends
from app.repositories.user_auth import UserAuthRepository
from app.services.user_auth import UserAuthService


def get_user_auth_repo() -> UserAuthRepository:
    return UserAuthRepository()


def get_user_auth_service(
    user_auth_repo: Annotated[UserAuthRepository, Depends(get_user_auth_repo)],
) -> UserAuthService:
    return UserAuthService(user_auth_repo)
