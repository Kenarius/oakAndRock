"""Common settings module."""
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    """Common postgres settings."""

    echo: bool = False

    @property
    def db_uri(self) -> str:
        """Return database uri."""

        SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "postgresql://neondb_owner:npg_7Lq4WPbCGOes@ep-snowy-voice-agbqqvf6-pooler.c-2.eu-central-1.aws.neon.tech/neondb")
        ASYNC_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        return ASYNC_DATABASE_URL


class AdminAuthSettings(BaseSettings):
    """Admin panel and API auth credentials from environment."""

    username: str = Field(default="admin", validation_alias="ADMIN_USERNAME")
    password: str = Field(default="password", validation_alias="ADMIN_PASSWORD")
    session_secret: str = Field(default="default_secret", validation_alias="ADMIN_SESSION_SECRET")
    jwt_secret: str | None = Field(default=None, validation_alias="ADMIN_JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", validation_alias="ADMIN_JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, validation_alias="ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES")

    model_config = SettingsConfigDict(
        env_file=[".env", ".env.prod"],
        populate_by_name=True,
        extra="ignore",
    )

    @property
    def effective_jwt_secret(self) -> str:
        return self.jwt_secret or self.session_secret


class OakSettings(BaseSettings):
    """Oak app settings class."""

    host: str = '0.0.0.0'
    port: str = '8000'
    secret_key: str = 'random-key-example-kjdhfkjshtdurkfu,ghvbfdhpt;oi@#27rgdjdr99hfsdjh89iukgjhryukjh3qrfedf'
    name: str = 'Oak'
    version: str = '1.0.0'
    description: str = 'Oak service'
    docs_prefix: str = '/oak'

    model_config = SettingsConfigDict(
        env_prefix="OAK_APP_",
        env_file=[".env", ".env.prod"],
        extra="ignore",
    )


class Settings(BaseSettings):
    """Settings of common package."""

    model_config = SettingsConfigDict(extra="ignore")

    postgres: PostgresSettings = PostgresSettings()
    oak_app: OakSettings = OakSettings()
    admin_auth: AdminAuthSettings = AdminAuthSettings()


settings = Settings()
