from __future__ import annotations

from pydantic import BaseModel, Field


class SupervisorAgentInput(BaseModel):
    session_id: str
    customer_id: str
    message: str
    context: dict = Field(default_factory=dict)


class SupervisorAgentOutput(BaseModel):
    agent: str
    message: str
    confidence: float = Field(ge=0.0, le=1.0)
    data: dict = Field(default_factory=dict)
    requires_escalation: bool = False
