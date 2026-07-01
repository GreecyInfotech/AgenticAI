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
    openai_embedding_model: str = "text-embedding-3-small"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    llm_max_retries: int = 3
    llm_timeout_seconds: float = 30.0
    memory_session_ttl_seconds: int = 86400
    memory_summary_threshold: int = 12
    qdrant_enabled: bool = True
    rag_bootstrap_on_startup: bool = True
    oauth_issuer: str = ""
    okta_domain: str = ""

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "distributor"
    postgres_password: str = "distributor_secret"
    postgres_db: str = "distributor_platform"
    postgres_min_pool: int = 2
    postgres_max_pool: int = 10
    postgres_command_timeout: int = 30
    postgres_ssl: bool = False

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0
    redis_ssl: bool = False
    redis_socket_timeout: float = 5.0

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "distributor_knowledge"
    qdrant_api_key: str = ""
    qdrant_https: bool = False

    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_enabled: bool = True
    kafka_consumer_group: str = "ai-platform"
    kafka_auto_create_topics: bool = True

    email_enabled: bool = True
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@distributor.local"
    smtp_use_tls: bool = True

    crm_provider: str = "mock"
    crm_base_url: str = ""
    crm_api_key: str = ""
    crm_timeout_seconds: float = 10.0

    otel_enabled: bool = False
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        auth = f":{self.redis_password}@" if self.redis_password else ""
        scheme = "rediss" if self.redis_ssl else "redis"
        return f"{scheme}://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
