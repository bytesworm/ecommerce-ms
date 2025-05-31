from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password
from app.models.user_auth import UserAuth
from app.repositories.user_auth import UserAuthRepository
from app.schemas.user_auth import UserAuthCreate, UserAuthRead


class UserAuthService:
    def __init__(self, repository: UserAuthRepository) -> None:
        self.repository = repository

    async def save(
        self, session: AsyncSession, user_auth: UserAuthCreate
    ) -> UserAuthRead:
        user_auth_db = await self.repository.get_by_email(session, user_auth.email)

        if user_auth_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already exists"
            )

        hashed_password = hash_password(user_auth.password)
        data = user_auth.model_dump()
        data["password"] = hashed_password
        user_auth_saved = await self.repository.save(session, UserAuth(**data))
        return UserAuthRead.model_validate(user_auth_saved)

    async def get_by_id(self, session: AsyncSession, id: int) -> UserAuthRead:
        user_auth_db = await self.repository.get_by_id(session, id)
        try:
            return UserAuthRead.model_validate(user_auth_db)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

    async def get_by_email(self, session: AsyncSession, email: str) -> UserAuthRead:
        user_auth_db = await self.repository.get_by_email(session, email)
        try:
            return UserAuthRead.model_validate(user_auth_db)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )
