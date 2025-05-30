from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
import jwt

from app.schemes.token import TokenData


class TokenService:
    def __init__(
        self, secret_key: str, algorithm: str, access_token_expire_minutes: int
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, data: TokenData) -> str:
        to_encode = data.model_dump()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_expire_minutes
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self, token: str) -> TokenData:
        payload = jwt.decode(token, self.secret_key, self.algorithm)
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(sub=email)
