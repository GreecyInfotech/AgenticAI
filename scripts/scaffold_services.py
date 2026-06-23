#!/usr/bin/env python3
"""Scaffold all Python services for Smart Port AI Platform."""

from pathlib import Path

ROOT = Path(__file__).parent.parent

AGENTS = {
    "vessel-agent": {
        "description": "Vessel scheduling, berth allocation, and ETA optimization agent",
        "domain": "vessel",
        "tools": ["get_vessel_schedule", "allocate_berth", "predict_eta", "get_weather_impact"],
        "kafka_topics": ["vessel.arrivals", "vessel.departures", "berth.allocations"],
    },
    "container-agent": {
        "description": "Container yard management and stacking optimization agent",
        "domain": "container",
        "tools": ["get_container_status", "optimize_stacking", "find_container", "plan_moves"],
        "kafka_topics": ["container.moves", "yard.status"],
    },
    "customs-agent": {
        "description": "Customs clearance and compliance automation agent",
        "domain": "customs",
        "tools": ["check_clearance", "submit_declaration", "validate_documents", "flag_risk"],
        "kafka_topics": ["customs.declarations", "customs.clearance"],
    },
    "billing-agent": {
        "description": "Port billing, invoicing, and revenue management agent",
        "domain": "billing",
        "tools": ["calculate_charges", "generate_invoice", "get_tariff", "reconcile_payments"],
        "kafka_topics": ["billing.invoices", "billing.payments"],
    },
    "maintenance-agent": {
        "description": "Equipment maintenance scheduling and predictive upkeep agent",
        "domain": "maintenance",
        "tools": ["schedule_maintenance", "get_equipment_health", "predict_failure", "create_work_order"],
        "kafka_topics": ["maintenance.work_orders", "equipment.health"],
    },
    "incident-agent": {
        "description": "Incident detection, triage, and resolution agent",
        "domain": "incident",
        "tools": ["detect_incident", "triage_incident", "escalate", "generate_report"],
        "kafka_topics": ["incidents.created", "incidents.resolved"],
    },
    "planning-agent": {
        "description": "Port operations planning and resource optimization agent",
        "domain": "planning",
        "tools": ["create_plan", "optimize_resources", "simulate_scenario", "get_capacity"],
        "kafka_topics": ["planning.schedules", "planning.optimizations"],
    },
    "safety-agent": {
        "description": "Safety compliance monitoring and hazard detection agent",
        "domain": "safety",
        "tools": ["check_compliance", "detect_hazard", "issue_alert", "audit_safety"],
        "kafka_topics": ["safety.alerts", "safety.audits"],
    },
    "weather-agent": {
        "description": "Weather impact analysis and operational advisory agent",
        "domain": "weather",
        "tools": ["get_forecast", "assess_impact", "recommend_action", "get_tide_info"],
        "kafka_topics": ["weather.forecasts", "weather.alerts"],
    },
    "logistics-agent": {
        "description": "Truck gate, drayage, and intermodal logistics agent",
        "domain": "logistics",
        "tools": ["schedule_gate", "optimize_routes", "track_shipment", "manage_queue"],
        "kafka_topics": ["logistics.gate", "logistics.shipments"],
    },
    "executive-agent": {
        "description": "Executive KPI synthesis and strategic decision support agent",
        "domain": "executive",
        "tools": ["get_kpis", "generate_briefing", "analyze_trends", "compare_benchmarks"],
        "kafka_topics": ["executive.briefings", "executive.kpis"],
    },
}

MCP_SERVERS = {
    "tos-mcp": {"description": "Terminal Operating System integration", "domain": "TOS"},
    "sap-mcp": {"description": "SAP ERP integration", "domain": "SAP"},
    "postgres-mcp": {"description": "PostgreSQL database access", "domain": "PostgreSQL"},
    "kafka-mcp": {"description": "Kafka event streaming", "domain": "Kafka"},
    "customs-mcp": {"description": "Customs authority systems", "domain": "Customs"},
    "vessel-tracking-mcp": {"description": "AIS vessel tracking", "domain": "VesselTracking"},
    "billing-mcp": {"description": "Billing and invoicing systems", "domain": "Billing"},
    "gate-mcp": {"description": "Gate and truck management", "domain": "Gate"},
    "crane-mcp": {"description": "Crane and equipment control", "domain": "Crane"},
    "weather-mcp": {"description": "Weather data services", "domain": "Weather"},
    "inventory-mcp": {"description": "Inventory and warehouse", "domain": "Inventory"},
    "monitoring-mcp": {"description": "Infrastructure monitoring", "domain": "Monitoring"},
}

RAG_SERVICES = {
    "document-ingestion": "Document upload, parsing, and preprocessing pipeline",
    "chunking": "Intelligent document chunking with semantic boundaries",
    "embedding-service": "Text embedding generation service",
    "vector-search": "Vector similarity search and retrieval",
    "metadata-extraction": "Document metadata and entity extraction",
    "knowledge-management": "Knowledge base CRUD and lifecycle management",
}

ML_SERVICES = {
    "vessel-delay-prediction": {"model": "vessel_delay", "features": ["vessel_type", "origin", "weather_score", "congestion_level"]},
    "berth-optimization": {"model": "berth_optimizer", "features": ["vessel_length", "draft", "cargo_type", "priority"]},
    "crane-failure-prediction": {"model": "crane_failure", "features": ["operating_hours", "load_cycles", "temperature", "vibration"]},
    "truck-queue-prediction": {"model": "truck_queue", "features": ["hour_of_day", "gate_id", "day_of_week", "container_count"]},
    "congestion-prediction": {"model": "congestion", "features": ["vessel_count", "container_moves", "truck_queue", "weather_score"]},
    "anomaly-detection": {"model": "anomaly", "features": ["metric_value", "baseline", "variance", "time_window"]},
    "revenue-forecasting": {"model": "revenue", "features": ["month", "vessel_calls", "teu_volume", "tariff_rate"]},
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def agent_pyproject(name: str, desc: str) -> str:
    return f'''[project]
name = "{name}"
version = "1.0.0"
description = "{desc}"
requires-python = ">=3.11"
dependencies = [
    "smart-port-common",
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "langchain>=0.3",
    "langchain-openai>=0.2",
    "langgraph>=0.2",
    "httpx>=0.27",
    "pydantic>=2.0",
]

[tool.uv.sources]
smart-port-common = {{ workspace = true }}

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
'''


def agent_main(name: str, domain: str, tools: list[str], port: int) -> str:
    tools_list = ", ".join(f'"{t}"' for t in tools)
    return f'''"""{name.replace("-", " ").title()} - FastAPI service entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from smart_port_common import create_health_router, get_settings, setup_logging, setup_telemetry
from smart_port_common.auth import TokenPayload, verify_token
from smart_port_common.logging import get_logger

from .agent import run_agent
from .config import AgentSettings

logger = get_logger(__name__)
settings = AgentSettings(service_name="{name}", service_port={port})


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
    logger.info("agent_starting", agent="{name}", domain="{domain}")
    yield
    logger.info("agent_stopping", agent="{name}")


app = FastAPI(
    title="{name.replace("-", " ").title()}",
    description="Smart Port AI Agent - {domain} domain",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(create_health_router("{name}"))
setup_telemetry(app, "{name}")

AVAILABLE_TOOLS = [{tools_list}]


@app.get("/tools")
async def list_tools(token: TokenPayload = verify_token) -> dict:
    return {{"tools": AVAILABLE_TOOLS, "domain": "{domain}"}}


@app.post("/invoke", response_model=AgentResponse)
async def invoke(payload: AgentRequest, token: TokenPayload = verify_token) -> AgentResponse:
    try:
        result = await run_agent(
            query=payload.query,
            context={{**payload.context, "user_id": token.sub, "roles": token.roles}},
            session_id=payload.session_id,
        )
        return AgentResponse(**result)
    except Exception as exc:
        logger.error("agent_invoke_failed", error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.service_port)
'''


def agent_impl(name: str, domain: str, tools: list[str]) -> str:
    tool_funcs = "\n\n".join(
        f'''@tool
def {t}(input_data: str) -> str:
    """Execute {t.replace("_", " ")} for {domain} operations."""
    return json.dumps({{"tool": "{t}", "domain": "{domain}", "result": "success", "data": input_data}})'''
        for t in tools
    )
    tool_names = ", ".join(tools)
    return f'''"""LangGraph agent implementation for {name}."""

import json
import uuid
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from smart_port_common.config import get_settings
from smart_port_common.logging import get_logger

from .config import AgentSettings

logger = get_logger(__name__)
settings = AgentSettings()

SYSTEM_PROMPT = """You are the Smart Port {domain.title()} Agent.
You help port operators with {domain}-related tasks including:
{chr(10).join(f"- {t.replace('_', ' ')}" for t in tools)}

Always provide actionable, data-driven recommendations.
Cite specific tool results when available. Be concise and professional."""


{tool_funcs}


def _get_llm() -> ChatOpenAI:
    cfg = get_settings()
    if cfg.azure_openai_endpoint:
        return ChatOpenAI(
            azure_endpoint=cfg.azure_openai_endpoint,
            api_key=cfg.azure_openai_api_key,
            azure_deployment=cfg.azure_openai_deployment,
            api_version="2024-02-01",
        )
    return ChatOpenAI(model="gpt-4o", api_key=cfg.openai_api_key or "not-set")


async def run_agent(
    query: str,
    context: dict[str, Any] | None = None,
    session_id: str | None = None,
) -> dict[str, Any]:
    context = context or {{}}
    session_id = session_id or str(uuid.uuid4())

    llm = _get_llm()
    tools = [{tool_names}]
    agent = create_react_agent(llm, tools)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Context: {{json.dumps(context)}}\\n\\nQuery: {{query}}"),
    ]

    logger.info("agent_invocation", session_id=session_id, query=query[:100])
    result = await agent.ainvoke({{"messages": messages}})

    final_message = result["messages"][-1].content
    tools_used = [
        tc.get("name", "") for msg in result["messages"]
        if hasattr(msg, "tool_calls") and msg.tool_calls
        for tc in (msg.tool_calls or [])
    ]

    return {{
        "answer": final_message,
        "tools_used": tools_used,
        "confidence": 0.85,
        "session_id": session_id,
        "metadata": {{"domain": "{domain}", "agent": "{name}"}},
    }}
'''


def agent_config(port: int) -> str:
    return f'''"""Agent-specific configuration."""

from smart_port_common.config import Settings


class AgentSettings(Settings):
    service_port: int = {port}
    max_iterations: int = 10
    mcp_server_url: str = "http://localhost:8090"
'''


def agent_dockerfile(name: str, port: int) -> str:
    return f'''FROM python:3.11-slim AS base
WORKDIR /app
RUN pip install uv

FROM base AS builder
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY agents/{name} /app/agents/{name}
COPY pyproject.toml /app/
WORKDIR /app/agents/{name}
RUN uv pip install --system -e . -e /app/shared/python/smart_port_common

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY agents/{name}/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE {port}
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}", "--app-dir", "/app/src"]
'''


def mcp_server_pyproject(name: str, desc: str) -> str:
    return f'''[project]
name = "{name}"
version = "1.0.0"
description = "{desc}"
requires-python = ">=3.11"
dependencies = [
    "smart-port-common",
    "mcp>=1.0",
    "httpx>=0.27",
    "pydantic>=2.0",
]

[tool.uv.sources]
smart-port-common = {{ workspace = true }}

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
'''


def mcp_server_impl(name: str, domain: str) -> str:
    return f'''"""MCP Server for {domain} integration."""

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from smart_port_common.logging import get_logger

logger = get_logger(__name__)
mcp = FastMCP("{name}")


@mcp.tool()
def query_{domain.lower()}(query: str) -> str:
    """Query {domain} system with natural language or structured query."""
    logger.info("mcp_query", server="{name}", query=query[:100])
    return json.dumps({{"domain": "{domain}", "query": query, "status": "success", "results": []}})


@mcp.tool()
def get_{domain.lower()}_status(resource_id: str) -> str:
    """Get status of a {domain} resource by ID."""
    return json.dumps({{"domain": "{domain}", "resource_id": resource_id, "status": "active"}})


@mcp.tool()
def list_{domain.lower()}_resources(filter_params: str = "{{}}") -> str:
    """List {domain} resources with optional filter parameters (JSON string)."""
    filters: dict[str, Any] = json.loads(filter_params) if filter_params else {{}}
    return json.dumps({{"domain": "{domain}", "filters": filters, "resources": [], "total": 0}})


@mcp.tool()
def execute_{domain.lower()}_action(action: str, payload: str = "{{}}") -> str:
    """Execute an action on the {domain} system."""
    data: dict[str, Any] = json.loads(payload) if payload else {{}}
    logger.info("mcp_action", server="{name}", action=action)
    return json.dumps({{"domain": "{domain}", "action": action, "payload": data, "status": "executed"}})


if __name__ == "__main__":
    mcp.run(transport="stdio")
'''


def rag_service(name: str, desc: str, port: int) -> None:
    base = ROOT / "rag" / name
    write(base / "pyproject.toml", f'''[project]
name = "{name}"
version = "1.0.0"
description = "{desc}"
requires-python = ">=3.11"
dependencies = [
    "smart-port-common",
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "httpx>=0.27",
    "pydantic>=2.0",
]

[tool.uv.sources]
smart-port-common = {{ workspace = true }}

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
''')
    write(base / "src" / "main.py", f'''"""{desc}"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from smart_port_common import create_health_router, setup_logging, setup_telemetry
from smart_port_common.auth import TokenPayload, verify_token
from smart_port_common.logging import get_logger

logger = get_logger(__name__)
SERVICE_NAME = "{name}"
SERVICE_PORT = {port}


class ProcessRequest(BaseModel):
    document_id: str | None = None
    content: str | None = None
    metadata: dict = Field(default_factory=dict)
    options: dict = Field(default_factory=dict)


class ProcessResponse(BaseModel):
    status: str
    document_id: str | None = None
    result: dict = Field(default_factory=dict)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(SERVICE_NAME)
    logger.info("service_starting", service=SERVICE_NAME)
    yield


app = FastAPI(title="{name}", description="{desc}", version="1.0.0", lifespan=lifespan)
app.include_router(create_health_router(SERVICE_NAME))
setup_telemetry(app, SERVICE_NAME)


@app.post("/process", response_model=ProcessResponse)
async def process(request: ProcessRequest, token: TokenPayload = verify_token) -> ProcessResponse:
    try:
        from .processor import process_document
        result = await process_document(request.model_dump())
        return ProcessResponse(status="success", document_id=request.document_id, result=result)
    except Exception as exc:
        logger.error("process_failed", error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
''')
    write(base / "src" / "processor.py", f'''"""Core processing logic for {name}."""

from typing import Any


async def process_document(data: dict[str, Any]) -> dict[str, Any]:
    """Process document through the {name} pipeline stage."""
    content = data.get("content", "")
    metadata = data.get("metadata", {{}})
    options = data.get("options", {{}})

    return {{
        "service": "{name}",
        "content_length": len(content) if content else 0,
        "metadata": metadata,
        "options": options,
        "processed": True,
    }}
''')
    write(base / "Dockerfile", f'''FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY rag/{name} /app/rag/{name}
RUN pip install -e /app/shared/python/smart_port_common -e /app/rag/{name}
COPY rag/{name}/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE {port}
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}", "--app-dir", "/app/src"]
''')


def ml_service(name: str, config: dict, port: int) -> None:
    base = ROOT / "ml-platform" / name
    features = config["features"]
    model = config["model"]
    write(base / "pyproject.toml", f'''[project]
name = "{name}"
version = "1.0.0"
description = "ML model service: {name}"
requires-python = ">=3.11"
dependencies = [
    "smart-port-common",
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "scikit-learn>=1.5",
    "numpy>=1.26",
    "pandas>=2.2",
    "joblib>=1.4",
    "pydantic>=2.0",
]

[tool.uv.sources]
smart-port-common = {{ workspace = true }}

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
''')
    feature_fields = "\n    ".join(f"{f}: float = 0.0" for f in features)
    write(base / "src" / "main.py", f'''"""ML inference service: {name}."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from smart_port_common import create_health_router, setup_logging, setup_telemetry
from smart_port_common.auth import TokenPayload, verify_token
from smart_port_common.logging import get_logger

from .model import load_model, predict

logger = get_logger(__name__)
SERVICE_NAME = "{name}"
SERVICE_PORT = {port}


class PredictionRequest(BaseModel):
    {feature_fields}


class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    model_version: str = "1.0.0"
    features_used: list[str] = Field(default_factory=lambda: {features!r})


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(SERVICE_NAME)
    load_model()
    logger.info("ml_service_started", model="{model}")
    yield


app = FastAPI(title="{name}", version="1.0.0", lifespan=lifespan)
app.include_router(create_health_router(SERVICE_NAME))
setup_telemetry(app, SERVICE_NAME)


@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(
    request: PredictionRequest, token: TokenPayload = verify_token
) -> PredictionResponse:
    features = request.model_dump()
    result = predict(features)
    return PredictionResponse(**result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
''')
    write(base / "src" / "model.py", f'''"""ML model for {name}."""

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

FEATURES = {features!r}
_model: GradientBoostingRegressor | None = None


def load_model() -> None:
    global _model
    _model = GradientBoostingRegressor(n_estimators=50, random_state=42)
    rng = np.random.RandomState(42)
    X = rng.rand(200, len(FEATURES))
    y = rng.rand(200) * 100
    _model.fit(X, y)


def predict(features: dict[str, float]) -> dict:
    if _model is None:
        load_model()
    X = np.array([[features.get(f, 0.0) for f in FEATURES]])
    prediction = float(_model.predict(X)[0])
    return {{
        "prediction": round(prediction, 4),
        "confidence": 0.82,
        "model_version": "1.0.0",
        "features_used": FEATURES,
    }}
''')
    write(base / "Dockerfile", f'''FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY ml-platform/{name} /app/ml-platform/{name}
RUN pip install -e /app/shared/python/smart_port_common -e /app/ml-platform/{name}
COPY ml-platform/{name}/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE {port}
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}", "--app-dir", "/app/src"]
''')


def scaffold_agents() -> None:
    base_port = 8100
    for i, (name, cfg) in enumerate(AGENTS.items()):
        port = base_port + i
        base = ROOT / "agents" / name
        write(base / "pyproject.toml", agent_pyproject(name, cfg["description"]))
        write(base / "src" / "main.py", agent_main(name, cfg["domain"], cfg["tools"], port))
        write(base / "src" / "agent.py", agent_impl(name, cfg["domain"], cfg["tools"]))
        write(base / "src" / "config.py", agent_config(port))
        write(base / "src" / "__init__.py", "")
        write(base / "Dockerfile", agent_dockerfile(name, port))
        write(base / "tests" / "test_agent.py", f'''"""Tests for {name}."""

import pytest
from fastapi.testclient import TestClient

from smart_port_common.auth import create_token


@pytest.fixture
def client():
    from main import app
    return TestClient(app)


@pytest.fixture
def auth_headers():
    token = create_token("test-user", roles=["operator"])
    return {{"Authorization": f"Bearer {{token}}"}}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_tools(client, auth_headers):
    response = client.get("/tools", headers=auth_headers)
    assert response.status_code == 200
    assert "tools" in response.json()
''')


def scaffold_mcp_servers() -> None:
    for name, cfg in MCP_SERVERS.items():
        base = ROOT / "mcp-servers" / name
        write(base / "pyproject.toml", mcp_server_pyproject(name, cfg["description"]))
        write(base / "src" / "server.py", mcp_server_impl(name, cfg["domain"]))
        write(base / "src" / "__init__.py", "")
        write(base / "Dockerfile", f'''FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY mcp-servers/{name} /app/mcp-servers/{name}
RUN pip install -e /app/shared/python/smart_port_common -e /app/mcp-servers/{name}
COPY mcp-servers/{name}/src /app/src
ENV PYTHONPATH=/app/src
CMD ["python", "/app/src/server.py"]
''')


def scaffold_rag() -> None:
    base_port = 8200
    for i, (name, desc) in enumerate(RAG_SERVICES.items()):
        rag_service(name, desc, base_port + i)


def scaffold_ml() -> None:
    base_port = 8300
    for i, (name, cfg) in enumerate(ML_SERVICES.items()):
        ml_service(name, cfg, base_port + i)


if __name__ == "__main__":
    scaffold_agents()
    scaffold_mcp_servers()
    scaffold_rag()
    scaffold_ml()
    print("Scaffolded all Python services successfully.")
