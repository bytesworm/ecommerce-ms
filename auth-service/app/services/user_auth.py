from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, verify_hash
from app.models.user_auth import UserAuth
from app.repositories.user_repository import UserAuthRepository
from app.schemes.user_auth import UserAuthCreate, UserAuthRead, UserAuthVerify


class UserAuthService:
    def __init__(self) -> None:
        self.user_auth_repo = UserAuthRepository()

    async def save(
        self, session: AsyncSession, user_auth: UserAuthCreate
    ) -> UserAuthRead:
        user_auth_db = await self.user_auth_repo.get_by_email(session, user_auth.email)

        if user_auth_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already exists"
            )

        hashed_password = hash_password(user_auth.password)
        data = user_auth.model_dump()
        data["password"] = hashed_password
        user_auth_saved = await self.user_auth_repo.save(session, UserAuth(**data))
        return UserAuthRead.model_validate(user_auth_saved)

    async def get_by_id(self, session: AsyncSession, id: int) -> UserAuthRead | None:
        user_auth_db = await self.user_auth_repo.get_by_id(session, id)
        return UserAuthRead.model_validate(user_auth_db)

    async def verify(self, session: AsyncSession, user_auth: UserAuthVerify) -> bool:
        user_auth_db = await self.user_auth_repo.get_by_email(session, user_auth.email)

        if not user_auth_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found by email"
            )

        return verify_hash(user_auth.password, user_auth_db.password)
