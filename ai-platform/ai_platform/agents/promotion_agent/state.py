from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.promotion_agent.schemas import PromotionAgentOutput


class PromotionAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: PromotionAgentOutput | None
    next_agent: str | None
