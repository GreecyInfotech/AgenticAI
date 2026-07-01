from __future__ import annotations

from pydantic import BaseModel, Field


class ConversationRequestDTO(BaseModel):
    session_id: str
    customer_id: str
    message: str = Field(min_length=1, max_length=4000)


class ConversationResponseDTO(BaseModel):
    session_id: str
    reply: str | None
    target_agent: str | None
    agent_results: list[dict] = Field(default_factory=list)
    requires_escalation: bool = False
