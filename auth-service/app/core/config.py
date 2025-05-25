from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    @property
    @computed_field
    def SQLALCHEMY_URI(cls) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=cls.POSTGRES_HOST,
            username=cls.POSTGRES_USER,
            password=cls.POSTGRES_PASSWORD,
            port=cls.POSTGRES_PORT
        )

settings = Settings()
