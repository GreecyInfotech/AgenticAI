from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.analytics_agent.schemas import AnalyticsAgentOutput


class AnalyticsAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: AnalyticsAgentOutput | None
    next_agent: str | None
