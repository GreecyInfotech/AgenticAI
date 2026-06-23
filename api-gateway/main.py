"""API Gateway — unified external API for B2B/B2C portals."""

from __future__ import annotations

from typing import Any

import httpx
from fastapi import HTTPException
from pydantic import BaseModel, Field

from eaap_platform.app_factory import create_service_app
from eaap_platform.config import get_settings

app = create_service_app("API Gateway", "1.0.0")


class AgentRunRequest(BaseModel):
    query: str = Field(..., min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)
    portal: str = "b2b"


class ChatRequest(BaseModel):
    messages: list[dict[str, str]]
    temperature: float = 0.2


async def _proxy_post(base_url: str, path: str, body: dict[str, Any]) -> Any:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f"{base_url.rstrip('/')}{path}", json=body)
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


async def _proxy_get(base_url: str, path: str) -> Any:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{base_url.rstrip('/')}{path}")
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.get("/")
async def root() -> dict[str, str]:
    return {"platform": "enterprise-agentic-ai-platform", "gateway": "api-gateway"}


@app.get("/services")
async def services() -> dict[str, str]:
    return get_settings().service_registry


@app.get("/agents")
async def list_agents() -> Any:
    settings = get_settings()
    return await _proxy_get(settings.agent_gateway_url, "/agents")


@app.post("/agents/{agent_id}/run")
async def run_agent(agent_id: str, request: AgentRunRequest) -> Any:
    settings = get_settings()
    return await _proxy_post(
        settings.agent_gateway_url,
        f"/agents/{agent_id}/run",
        {"query": request.query, "context": {**request.context, "portal": request.portal}},
    )


@app.post("/rag/ingest")
async def rag_ingest(body: dict[str, Any]) -> Any:
    settings = get_settings()
    return await _proxy_post(settings.rag_service_url, "/ingest", body)


@app.post("/rag/search")
async def rag_search(body: dict[str, Any]) -> Any:
    settings = get_settings()
    return await _proxy_post(settings.rag_service_url, "/search", body)


@app.get("/orders")
async def list_orders() -> Any:
    from postgres.client import PostgresClient

    return {"orders": PostgresClient().list_orders()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
