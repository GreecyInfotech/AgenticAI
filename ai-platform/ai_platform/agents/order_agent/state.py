from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.order_agent.schemas import OrderAgentOutput


class OrderAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: OrderAgentOutput | None
    next_agent: str | None
