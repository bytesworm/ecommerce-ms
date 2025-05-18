from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def save(self, session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.add(user)
        await session.refresh(user)
        return user
