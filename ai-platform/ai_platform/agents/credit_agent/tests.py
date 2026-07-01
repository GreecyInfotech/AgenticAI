from __future__ import annotations

import pytest

from ai_platform.agents.credit_agent.agent import CreditAgent
from ai_platform.agents.credit_agent.schemas import CreditAgentInput


@pytest.mark.asyncio
async def test_credit_agent_run() -> None:
    agent = CreditAgent()
    result = await agent.run(
        CreditAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "credit_agent"
    assert result.confidence > 0
