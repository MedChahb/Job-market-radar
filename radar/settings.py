"""Settings, read from environment variables or a local .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Every setting uses the RADAR_ prefix, for example RADAR_DATABASE_URL."""

    model_config = SettingsConfigDict(env_prefix="RADAR_", env_file=".env", extra="ignore")

    # Defaults match the local Docker Compose database. Production values come from secrets.
    database_url: str = "postgresql://radar:radar@localhost:5433/radar"
    ollama_url: str = "http://localhost:11434"


@lru_cache
def get_settings() -> Settings:
    return Settings()
