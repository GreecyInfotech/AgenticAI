from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    """Shared environment configuration for all platform services."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_name: str = "ai-distributor-ordering-platform"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "distributor"
    postgres_password: str = "distributor_secret"
    postgres_db: str = "distributor_platform"

    redis_host: str = "localhost"
    redis_port: int = 6379

    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_enabled: bool = True

    jwt_secret: str = Field(default="change-me-in-production", min_length=8)
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    otel_enabled: bool = False
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def asyncpg_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"


@lru_cache
def get_base_settings() -> BaseServiceSettings:
    return BaseServiceSettings()
