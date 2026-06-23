"""Agent Gateway — orchestrates specialized enterprise agents."""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, Field

from agents.runner import AGENT_REGISTRY, run_agent as execute_agent
from eaap_platform.app_factory import create_service_app

app = create_service_app("Agent Gateway", "1.0.0")


class AgentRequest(BaseModel):
    query: str = Field(..., min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    agent: str
    answer: str
    actions_taken: list[str]
    metadata: dict[str, Any]


@app.get("/agents")
async def list_agents() -> list[dict[str, str]]:
    return [
        {"id": agent_id, "name": spec["name"], "description": spec["description"]}
        for agent_id, spec in AGENT_REGISTRY.items()
    ]


@app.post("/agents/{agent_id}/run", response_model=AgentResponse)
async def run_agent(agent_id: str, request: AgentRequest) -> AgentResponse:
    if agent_id not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    result = await execute_agent(agent_id, request.query, request.context)
    return AgentResponse(**result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
