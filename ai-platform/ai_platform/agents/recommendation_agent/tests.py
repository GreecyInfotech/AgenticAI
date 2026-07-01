from __future__ import annotations

import pytest

from ai_platform.agents.recommendation_agent.agent import RecommendationAgent
from ai_platform.agents.recommendation_agent.schemas import RecommendationAgentInput


@pytest.mark.asyncio
async def test_recommendation_agent_run() -> None:
    agent = RecommendationAgent()
    result = await agent.run(
        RecommendationAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "recommendation_agent"
    assert result.confidence > 0
