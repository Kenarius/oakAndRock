"""Common settings module."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    """Common postgres settings."""

    driver: str = ""
    user: str = "postgres"
    password: str = "postgres"
    db: str = "postgres"
    host: str = "0.0.0.0"
    echo: bool = False

    @property
    def db_uri(self) -> str:
        """Return database uri."""
        return f"{self.driver}://{self.user}:{self.password}@{self.host}/{self.db}"

    model_config = SettingsConfigDict(env_prefix="POSTGRES_", env_file=[".env", ".env.prod"])


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
