from __future__ import annotations

from ai_platform.agents.shipment_agent.schemas import ShipmentAgentInput


def build_prompt(input_data: ShipmentAgentInput) -> str:
    return (
        "You are the shipment agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
