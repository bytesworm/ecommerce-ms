from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class UserAuth(Base):
    __tablename__ = "user_auth"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

