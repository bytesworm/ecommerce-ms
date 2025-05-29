from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_current_user, get_db
from app.schemes.user_auth import UserAuthCreate, UserAuthRead
from app.services.user_auth import UserAuthService


router = APIRouter(prefix="/user-auth", tags=["UserAuth"])


@router.get("")
async def get_user_auth(
    id: int,
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserAuthRead | None:
    return await user_auth_service.get_by_id(db, id)


@router.post("")
async def create_user_auth(
    user_auth: UserAuthCreate,
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserAuthRead:
    return await user_auth_service.save(db, user_auth)

@router.get("/me")
async def get_me(
    current_user: Annotated[UserAuthRead, Depends(get_current_user)]
) -> UserAuthRead:
    return current_user
