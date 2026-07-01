from __future__ import annotations

from ai_platform.agents.supervisor_agent.schemas import SupervisorAgentInput
from ai_platform.prompts.loader import render_template


def build_prompt(input_data: SupervisorAgentInput) -> str:
    return render_template(
        "templates/supervisor_agent.j2",
        customer_id=input_data.customer_id,
        session_id=input_data.session_id,
        message=input_data.message,
        memory_summary=input_data.context.get("memory_summary", ""),
    )
