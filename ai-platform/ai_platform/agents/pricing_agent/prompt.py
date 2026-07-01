from __future__ import annotations

from ai_platform.agents.pricing_agent.schemas import PricingAgentInput


def build_prompt(input_data: PricingAgentInput) -> str:
    return (
        "You are the pricing agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
