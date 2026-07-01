from __future__ import annotations

import pytest

from ai_platform.agents.inventory_agent.agent import InventoryAgent
from ai_platform.agents.inventory_agent.schemas import InventoryAgentInput


@pytest.mark.asyncio
async def test_inventory_agent_run() -> None:
    agent = InventoryAgent()
    result = await agent.run(
        InventoryAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "inventory_agent"
    assert result.confidence > 0
