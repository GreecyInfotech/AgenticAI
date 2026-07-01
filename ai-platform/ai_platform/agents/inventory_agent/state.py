from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.inventory_agent.schemas import InventoryAgentOutput


class InventoryAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: InventoryAgentOutput | None
    next_agent: str | None
