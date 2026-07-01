from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.credit_agent.schemas import CreditAgentOutput


class CreditAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: CreditAgentOutput | None
    next_agent: str | None
