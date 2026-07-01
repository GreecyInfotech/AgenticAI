from __future__ import annotations

from ai_platform.agents.supervisor_agent.schemas import SupervisorAgentInput


def build_prompt(input_data: SupervisorAgentInput) -> str:
    return (
        "You are the supervisor agent for a distributor ordering platform.\n"
        f"Customer: {input_data.customer_id}\n"
        f"Request: {input_data.message}\n"
        "Respond with actionable distributor ordering guidance."
    )
