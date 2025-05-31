from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_hash
from app.repositories.user_repository import UserAuthRepository
from app.schemas.auth import AuthRequest
from app.schemas.token import Token, TokenData
from app.services.token import TokenService


class AuthService:
    def __init__(self, token_service: TokenService) -> None:
        self.token_service = token_service
        self.user_auth_repo = UserAuthRepository()

    async def auth(self, session: AsyncSession, auth_data: AuthRequest) -> Token:
        user_auth_db = await self.user_auth_repo.get_by_email(session, auth_data.email)

        if not user_auth_db or not verify_hash(
            auth_data.password, user_auth_db.password
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incorrect email or password",
            )

        token_data = TokenData(sub=auth_data.email)
        token = self.token_service.create_access_token(token_data)
        return Token(access_token=token, token_type="Bearer")
