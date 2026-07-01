from __future__ import annotations

from ai_platform.agents.document_agent.schemas import DocumentAgentInput


def build_prompt(input_data: DocumentAgentInput) -> str:
    return (
        "You are the document agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
