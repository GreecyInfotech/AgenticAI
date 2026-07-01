from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.payment_agent.schemas import PaymentAgentOutput


class PaymentAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: PaymentAgentOutput | None
    next_agent: str | None
