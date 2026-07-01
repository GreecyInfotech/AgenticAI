from __future__ import annotations

from ai_platform.agents.order_agent.schemas import OrderAgentInput


def build_prompt(input_data: OrderAgentInput) -> str:
    return (
        "You are the order agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
