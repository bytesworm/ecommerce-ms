from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db
from app.schemas.user_auth import UserAuthCreate, UserAuthRead
from app.services.user_auth import UserAuthService


router = APIRouter(prefix="/auth")


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
