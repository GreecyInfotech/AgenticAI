from __future__ import annotations

import pytest

from ai_platform.agents.customer_agent.agent import CustomerAgent
from ai_platform.agents.customer_agent.schemas import CustomerAgentInput


@pytest.mark.asyncio
async def test_customer_agent_run() -> None:
    agent = CustomerAgent()
    result = await agent.run(
        CustomerAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "customer_agent"
    assert result.confidence > 0
