"""Common settings module."""
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    """Common postgres settings."""

    echo: bool = False

    @property
    def db_uri(self) -> str:
        """Return database uri."""

        SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "0.0.0.0")
        ASYNC_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        return ASYNC_DATABASE_URL


class OakSettings(BaseSettings):
    """Oak app settings class."""

    host: str = '0.0.0.0'
    port: str = '8000'
    secret_key: str = 'random-key-example-kjdhfkjshtdurkfu,ghvbfdhpt;oi@#27rgdjdr99hfsdjh89iukgjhryukjh3qrfedf'
    name: str = 'Oak'
    version: str = '1.0.0'
    description: str = 'Oak service'
    docs_prefix: str = '/oak'

    model_config = SettingsConfigDict(env_prefix="OAK_APP_", env_file=[".env", ".env.prod"])


class Settings(BaseSettings):
    """Settings of common package."""

    postgres: PostgresSettings = PostgresSettings()
    oak_app: OakSettings = OakSettings()


settings = Settings()
