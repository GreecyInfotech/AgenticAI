"""Audit logging service."""

import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class AuditEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    action: str
    resource_type: str | None = None
    resource_id: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)
    ip_address: str | None = None
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class AuditLogger:
    """Records security-relevant actions for compliance."""

    async def log(self, entry: AuditEntry) -> None:
        # Production: persist to postgres audit_log table via postgres-mcp
        print(f"AUDIT: {entry.model_dump_json()}")  # noqa: T201

    async def log_agent_invocation(
        self, user_id: str, agent: str, query: str, ip: str | None = None
    ) -> None:
        await self.log(AuditEntry(
            user_id=user_id,
            action="agent.invoke",
            resource_type="agent",
            resource_id=agent,
            details={"query_length": len(query)},
            ip_address=ip,
        ))

    async def log_data_access(
        self, user_id: str, resource_type: str, resource_id: str, ip: str | None = None
    ) -> None:
        await self.log(AuditEntry(
            user_id=user_id,
            action="data.access",
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip,
        ))
