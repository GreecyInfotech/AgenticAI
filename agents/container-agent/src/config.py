"""Agent-specific configuration."""

from smart_port_common.config import Settings


class AgentSettings(Settings):
    service_port: int = 8101
    max_iterations: int = 10
    mcp_server_url: str = "http://localhost:8090"
