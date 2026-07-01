from __future__ import annotations

from typing import Protocol

from ai_platform.prompts.loader import render_template


class DomainAgentInput(Protocol):
    session_id: str
    customer_id: str
    message: str
    context: dict


def build_domain_prompt(agent_name: str, input_data: DomainAgentInput) -> str:
    return render_template(
        "templates/domain_agent.j2",
        agent_name=agent_name.replace("_", " "),
        customer_id=input_data.customer_id,
        session_id=input_data.session_id,
        message=input_data.message,
        memory_summary=input_data.context.get("memory_summary", ""),
    )
