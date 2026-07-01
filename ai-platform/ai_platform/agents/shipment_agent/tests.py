from __future__ import annotations

import pytest

from ai_platform.agents.shipment_agent.agent import ShipmentAgent
from ai_platform.agents.shipment_agent.schemas import ShipmentAgentInput


@pytest.mark.asyncio
async def test_shipment_agent_run() -> None:
    agent = ShipmentAgent()
    result = await agent.run(
        ShipmentAgentInput(session_id="s1", customer_id="CUST-001", message="test")
    )
    assert result.agent == "shipment_agent"
    assert result.confidence > 0
