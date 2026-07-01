from __future__ import annotations

from ai_platform.agents.payment_agent.schemas import PaymentAgentInput


def build_prompt(input_data: PaymentAgentInput) -> str:
    return (
        "You are the payment agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
