from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_auth import UserAuth


class UserAuthRepository:
    async def save(self, session: AsyncSession, user_auth: UserAuth) -> UserAuth:
        session.add(user_auth)
        await session.commit()
        await session.refresh(user_auth)
        return user_auth

    async def get_by_id(self, session: AsyncSession, id: int) -> UserAuth | None:
        stmt = select(UserAuth).where(UserAuth.id == id)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()
