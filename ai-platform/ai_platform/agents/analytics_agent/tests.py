from __future__ import annotations

import pytest

from ai_platform.agents.analytics_agent.agent import AnalyticsAgent
from ai_platform.agents.analytics_agent.schemas import AnalyticsAgentInput


@pytest.mark.asyncio
async def test_analytics_agent_run() -> None:
    agent = AnalyticsAgent()
    result = await agent.run(
        AnalyticsAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "analytics_agent"
    assert result.confidence > 0
