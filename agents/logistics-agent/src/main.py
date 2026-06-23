"""Logistics Agent - FastAPI service entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from smart_port_common import create_health_router, get_settings, setup_logging, setup_telemetry
from smart_port_common.auth import TokenPayload, verify_token
from smart_port_common.logging import get_logger

from agent import run_agent
from config import AgentSettings

logger = get_logger(__name__)
settings = AgentSettings(service_name="logistics-agent", service_port=8109)


class AgentRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    context: dict = Field(default_factory=dict)
    session_id: str | None = None


class AgentResponse(BaseModel):
    answer: str
    tools_used: list[str] = []
    confidence: float = 0.0
    session_id: str | None = None
    metadata: dict = Field(default_factory=dict)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.service_name, settings.log_level)
    logger.info("agent_starting", agent="logistics-agent", domain="logistics")
    yield
    logger.info("agent_stopping", agent="logistics-agent")


app = FastAPI(
    title="Logistics Agent",
    description="Smart Port AI Agent - logistics domain",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(create_health_router("logistics-agent"))
setup_telemetry(app, "logistics-agent")

AVAILABLE_TOOLS = ["schedule_gate", "optimize_routes", "track_shipment", "manage_queue"]


@app.get("/tools")
async def list_tools(token: TokenPayload = verify_token) -> dict:
    return {"tools": AVAILABLE_TOOLS, "domain": "logistics"}


@app.post("/invoke", response_model=AgentResponse)
async def invoke(payload: AgentRequest, token: TokenPayload = verify_token) -> AgentResponse:
    try:
        result = await run_agent(
            query=payload.query,
            context={**payload.context, "user_id": token.sub, "roles": token.roles},
            session_id=payload.session_id,
        )
        return AgentResponse(**result)
    except Exception as exc:
        logger.error("agent_invoke_failed", error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.service_port)
