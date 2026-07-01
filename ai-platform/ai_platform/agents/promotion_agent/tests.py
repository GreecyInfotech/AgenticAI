from __future__ import annotations

import pytest

from ai_platform.agents.promotion_agent.agent import PromotionAgent
from ai_platform.agents.promotion_agent.schemas import PromotionAgentInput


@pytest.mark.asyncio
async def test_promotion_agent_run() -> None:
    agent = PromotionAgent()
    result = await agent.run(
        PromotionAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "promotion_agent"
    assert result.confidence > 0
