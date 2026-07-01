from __future__ import annotations

import pytest

from ai_platform.agents.supervisor_agent.agent import SupervisorAgent
from ai_platform.agents.supervisor_agent.schemas import SupervisorAgentInput


@pytest.mark.asyncio
async def test_supervisor_agent_run() -> None:
    agent = SupervisorAgent()
    result = await agent.run(
        SupervisorAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "supervisor_agent"
    assert result.confidence > 0
