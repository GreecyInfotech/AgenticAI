from __future__ import annotations

from ai_platform.agents.knowledge_agent.schemas import KnowledgeAgentInput
from ai_platform.prompts.loader import render_template


def build_prompt(input_data: KnowledgeAgentInput) -> str:
    return render_template(
        "templates/knowledge_agent.j2",
        customer_id=input_data.customer_id,
        message=input_data.message,
        rag_context=input_data.context.get("rag_context", ""),
    )
