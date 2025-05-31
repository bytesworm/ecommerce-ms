from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.deps import get_current_user
from app.schemas.user_auth import UserAuthCreate, UserAuthRead
from app.services.user_auth import UserAuthService


router = APIRouter(prefix="/user-auth", tags=["UserAuth"])


@router.get(
    "",
    responses={
        404: {
            "description": "UserAuth not found",
            "content": {"application/json": {"example": {"detail": "Not found"}}},
        }
    },
)
async def get_user_auth(
    id: int,
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserAuthRead | None:
    return await user_auth_service.get_by_id(db, id)


@router.post(
    "",
    responses={
        409: {
            "description": "UserAuth already exists",
            "content": {"application/json": {"example": {"detail": "Already exists"}}},
        }
    },
)
async def create_user_auth(
    user_auth: UserAuthCreate,
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserAuthRead:
    return await user_auth_service.save(db, user_auth)


@router.get(
    "/me",
    description="Get current UserAuth by token",
    responses={
        401: {
            "description": "Invalid token provided",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        }
    },
)
async def get_me(
    current_user: Annotated[UserAuthRead, Depends(get_current_user)],
) -> UserAuthRead:
    return current_user
