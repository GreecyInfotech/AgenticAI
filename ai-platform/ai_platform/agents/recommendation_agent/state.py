from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.recommendation_agent.schemas import RecommendationAgentOutput


class RecommendationAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: RecommendationAgentOutput | None
    next_agent: str | None
