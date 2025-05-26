from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(str(settings.SQLALCHEMY_URI))

SessionLocal = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass
