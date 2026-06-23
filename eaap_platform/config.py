"""Platform-wide configuration."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PlatformSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"

    api_gateway_url: str = "http://localhost:8000"
    agent_gateway_url: str = "http://localhost:8001"
    rag_service_url: str = "http://localhost:8002"

    database_url: str = "postgresql://postgres:postgres@localhost:5432/eaap"
    database_sync_url: str = ""
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_agent_events_topic: str = "agent-events"
    kafka_order_events_topic: str = "order-events"

    chroma_persist_dir: str = "./data/chroma"
    chroma_collection: str = "eaap_knowledge"
    filesystem_mcp_root: str = "./data/files"

    jira_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""
    github_token: str = ""
    github_org: str = ""

    gemini_model: str = "gemini-2.0-flash"
    use_vertex_ai: bool = False

    otel_exporter_endpoint: str = "http://localhost:4318"
    prometheus_port: int = 9090

    service_registry: dict[str, str] = Field(default_factory=dict)

    def model_post_init(self, __context: object) -> None:
        if not self.database_sync_url:
            url = self.database_url
            if url.startswith("postgresql+asyncpg://"):
                url = url.replace("postgresql+asyncpg://", "postgresql://", 1)
            self.database_sync_url = url
        if not self.service_registry:
            self.service_registry = {
                "api-gateway": self.api_gateway_url,
                "agent-gateway": self.agent_gateway_url,
                "rag": self.rag_service_url,
            }


@lru_cache
def get_settings() -> PlatformSettings:
    return PlatformSettings()
