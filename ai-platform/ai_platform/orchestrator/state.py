from __future__ import annotations

from typing import Any, TypedDict

from pydantic import BaseModel, Field


class OrchestratorStateModel(BaseModel):
    session_id: str
    customer_id: str
    message: str
    target_agent: str | None = None
    agent_results: list[dict[str, Any]] = Field(default_factory=list)
    reply: str | None = None
    requires_escalation: bool = False
    memory_summary: str = ""
    rag_context: str = ""
    conversation_history: list[dict[str, str]] = Field(default_factory=list)

    def to_graph_state(self) -> dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_graph_state(cls, state: dict[str, Any]) -> OrchestratorStateModel:
        return cls(**{k: v for k, v in state.items() if k in cls.model_fields})


class OrchestratorState(TypedDict):
    session_id: str
    customer_id: str
    message: str
    target_agent: str | None
    agent_results: list[dict[str, Any]]
    reply: str | None
    requires_escalation: bool
    memory_summary: str
    rag_context: str
    conversation_history: list[dict[str, str]]
