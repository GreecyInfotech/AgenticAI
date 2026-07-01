from __future__ import annotations

from ai_platform.agents.recommendation_agent.schemas import RecommendationAgentInput


def build_prompt(input_data: RecommendationAgentInput) -> str:
    return (
        "You are the recommendation agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
