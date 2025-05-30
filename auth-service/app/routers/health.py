from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check(db: Annotated[AsyncSession, Depends(get_db)]) -> dict[str, str]:
    return {"status": "ok"}
