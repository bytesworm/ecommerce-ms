from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
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

        user_auth_model = UserAuth(**user_auth.model_dump())  # TODO: hash password
        user_auth_db = await self.user_auth_repo.save(session, user_auth_model)
        return UserAuthRead.model_validate(user_auth_db)

    async def get_by_id(self, session: AsyncSession, id: int) -> UserAuthRead | None:
        user_auth_db = await self.user_auth_repo.get_by_id(session, id)
        return UserAuthRead.model_validate(user_auth_db)
