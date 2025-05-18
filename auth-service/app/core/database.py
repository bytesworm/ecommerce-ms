from sqlalchemy.orm import DeclarativeBase, declarative_base
from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
