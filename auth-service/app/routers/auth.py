from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_auth_service, get_db
from app.schemes.auth import AuthRequest
from app.schemes.token import Token
from app.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", responses={
        404: {
            "description": "Invalid credentials",
            "content": {"application/json": {"example": {"detail": "Incorrect email or password"}}},
        }
    },)
async def auth(
    db: Annotated[AsyncSession, Depends(get_db)],
    auth_data: AuthRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    return await auth_service.auth(db, auth_data)
