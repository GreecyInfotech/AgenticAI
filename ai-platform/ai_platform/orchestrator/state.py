from __future__ import annotations

from typing import Any, TypedDict


class OrchestratorState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    target_agent: str | None
    agent_results: list[dict[str, Any]]
    reply: str | None
    requires_escalation: bool
