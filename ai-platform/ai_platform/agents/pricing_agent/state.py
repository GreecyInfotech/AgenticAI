from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.pricing_agent.schemas import PricingAgentOutput


class PricingAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: PricingAgentOutput | None
    next_agent: str | None
