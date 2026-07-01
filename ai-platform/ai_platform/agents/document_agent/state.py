from __future__ import annotations

from typing import TypedDict

from ai_platform.agents.document_agent.schemas import DocumentAgentOutput


class DocumentAgentState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    result: DocumentAgentOutput | None
    next_agent: str | None
