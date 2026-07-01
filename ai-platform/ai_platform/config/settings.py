from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_name: str = "ai-distributor-ordering-platform"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    llm_provider: str = "openai"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    ollama_base_url: str = "http://localhost:11434"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "distributor"
    postgres_password: str = "distributor_secret"
    postgres_db: str = "distributor_platform"

    redis_host: str = "localhost"
    redis_port: int = 6379

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "distributor_knowledge"

    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_enabled: bool = True

    otel_enabled: bool = False
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60


@lru_cache
def get_settings() -> Settings:
    return Settings()
