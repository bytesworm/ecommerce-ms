from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_auth import UserAuth
from app.repositories.user_repository import UserAuthRepository
from app.schemas.user_auth import UserAuthCreate, UserAuthRead


class UserAuthService:
    def __init__(self, user_auth_repo: UserAuthRepository):
        self.user_auth_repo = user_auth_repo

    async def save(
        self, session: AsyncSession, user_auth: UserAuthCreate
    ) -> UserAuthRead:
        if await self.user_auth_repo.exists_by_email(session, user_auth.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already exists"
            )

        user_auth_model = UserAuth(**user_auth.model_dump())
        user_auth_db = await self.user_auth_repo.save(session, user_auth_model)
        return UserAuthRead.model_validate(user_auth_db)
