from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.customer_agent.schemas import CustomerAgentOutput


class CustomerAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: CustomerAgentOutput | None
    next_agent: str | None
