from __future__ import annotations

from ai_platform.agents.credit_agent.schemas import CreditAgentInput


def build_prompt(input_data: CreditAgentInput) -> str:
    return (
        "You are the credit agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
