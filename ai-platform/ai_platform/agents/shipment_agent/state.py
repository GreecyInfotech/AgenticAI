from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.shipment_agent.schemas import ShipmentAgentOutput


class ShipmentAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: ShipmentAgentOutput | None
    next_agent: str | None
