from __future__ import annotations

import pytest

from ai_platform.agents.payment_agent.agent import PaymentAgent
from ai_platform.agents.payment_agent.schemas import PaymentAgentInput


@pytest.mark.asyncio
async def test_payment_agent_run() -> None:
    agent = PaymentAgent()
    result = await agent.run(
        PaymentAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "payment_agent"
    assert result.confidence > 0
