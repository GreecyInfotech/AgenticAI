from __future__ import annotations

from ai_platform.agents.knowledge_agent.schemas import KnowledgeAgentInput


def build_prompt(input_data: KnowledgeAgentInput) -> str:
    return (
        "You are the knowledge agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
