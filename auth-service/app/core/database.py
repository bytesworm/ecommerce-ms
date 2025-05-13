from sqlalchemy.orm import declarative_base
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)

Base = declarative_base()
