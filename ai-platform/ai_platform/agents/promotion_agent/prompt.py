from __future__ import annotations

from ai_platform.agents.promotion_agent.schemas import PromotionAgentInput


def build_prompt(input_data: PromotionAgentInput) -> str:
    return (
        "You are the promotion agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
