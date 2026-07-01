from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.knowledge_agent.schemas import KnowledgeAgentOutput


class KnowledgeAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: KnowledgeAgentOutput | None
    next_agent: str | None
