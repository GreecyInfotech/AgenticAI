from __future__ import annotations

from ai_platform.agents.inventory_agent.schemas import InventoryAgentInput


def build_prompt(input_data: InventoryAgentInput) -> str:
    return (
        "You are the inventory agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
