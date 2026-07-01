from __future__ import annotations

import pytest

from ai_platform.agents.pricing_agent.agent import PricingAgent
from ai_platform.agents.pricing_agent.schemas import PricingAgentInput


@pytest.mark.asyncio
async def test_pricing_agent_run() -> None:
    agent = PricingAgent()
    result = await agent.run(
        PricingAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "pricing_agent"
    assert result.confidence > 0
