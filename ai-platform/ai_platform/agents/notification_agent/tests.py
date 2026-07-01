from __future__ import annotations

import pytest

from ai_platform.agents.notification_agent.agent import NotificationAgent
from ai_platform.agents.notification_agent.schemas import NotificationAgentInput


@pytest.mark.asyncio
async def test_notification_agent_run() -> None:
    agent = NotificationAgent()
    result = await agent.run(
        NotificationAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "notification_agent"
    assert result.confidence > 0
