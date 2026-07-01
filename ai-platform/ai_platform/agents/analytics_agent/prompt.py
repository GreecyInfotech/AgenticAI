from __future__ import annotations

from ai_platform.agents.analytics_agent.schemas import AnalyticsAgentInput


def build_prompt(input_data: AnalyticsAgentInput) -> str:
    return (
        "You are the analytics agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
