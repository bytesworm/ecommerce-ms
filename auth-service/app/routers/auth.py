from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_auth_service
from app.schemas.auth import AuthRequest
from app.schemas.token import Token
from app.services.auth import AuthService


router = APIRouter(tags=["Auth"])


@router.post(
    "/login",
    responses={
        404: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"}
                }
            },
        }
    },
)
async def auth(
    db: Annotated[AsyncSession, Depends(get_db)],
    auth_data: AuthRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    return await auth_service.auth(db, auth_data)
