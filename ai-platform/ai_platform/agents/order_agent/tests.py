from __future__ import annotations

import pytest

from ai_platform.agents.order_agent.agent import OrderAgent
from ai_platform.agents.order_agent.schemas import OrderAgentInput


@pytest.mark.asyncio
async def test_order_agent_run() -> None:
    agent = OrderAgent()
    result = await agent.run(
        OrderAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "order_agent"
    assert result.confidence > 0
