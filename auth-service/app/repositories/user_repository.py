from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserRepository:
    async def save(self, session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
