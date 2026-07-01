from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.supervisor_agent.schemas import SupervisorAgentOutput


class SupervisorAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: SupervisorAgentOutput | None
    next_agent: str | None
