from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password
from app.models.user_auth import UserAuth
from app.repositories.user_repository import UserAuthRepository
from app.schemes.user_auth import UserAuthCreate, UserAuthRead


class UserAuthService:
    def __init__(self) -> None:
        self.user_auth_repo = UserAuthRepository()

    async def save(
        self, session: AsyncSession, user_auth: UserAuthCreate
    ) -> UserAuthRead:
        if await self.user_auth_repo.exists_by_email(session, user_auth.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already exists"
            )

        hashed_password = hash_password(user_auth.password)
        data = user_auth.model_dump()
        data["password"] = hashed_password
        user_auth_db = await self.user_auth_repo.save(session, UserAuth(**data))
        return UserAuthRead.model_validate(user_auth_db)

    async def get_by_id(self, session: AsyncSession, id: int) -> UserAuthRead | None:
        user_auth_db = await self.user_auth_repo.get_by_id(session, id)
        return UserAuthRead.model_validate(user_auth_db)
