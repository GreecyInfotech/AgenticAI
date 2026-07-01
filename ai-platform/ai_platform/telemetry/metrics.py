from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from prometheus_client import Counter, Histogram

LLM_REQUESTS = Counter(
    "ai_platform_llm_requests_total",
    "Total LLM invocations",
    ["provider", "success"],
)
LLM_LATENCY = Histogram(
    "ai_platform_llm_latency_seconds",
    "LLM invocation latency",
    ["provider"],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0),
)
AGENT_INVOCATIONS = Counter(
    "ai_platform_agent_invocations_total",
    "Agent invocations",
    ["agent", "success"],
)
ORCHESTRATOR_ROUTES = Counter(
    "ai_platform_orchestrator_routes_total",
    "Orchestrator routing decisions",
    ["target_agent"],
)
RAG_RETRIEVALS = Counter(
    "ai_platform_rag_retrievals_total",
    "RAG retrieval operations",
    ["source"],
)


def record_llm_request(provider: str, *, success: bool, latency: float) -> None:
    LLM_REQUESTS.labels(provider=provider, success=str(success).lower()).inc()
    LLM_LATENCY.labels(provider=provider).observe(latency)


def record_agent_invocation(agent: str, *, success: bool) -> None:
    AGENT_INVOCATIONS.labels(agent=agent, success=str(success).lower()).inc()


def record_orchestrator_route(target_agent: str) -> None:
    ORCHESTRATOR_ROUTES.labels(target_agent=target_agent).inc()


def record_rag_retrieval(source: str) -> None:
    RAG_RETRIEVALS.labels(source=source).inc()
