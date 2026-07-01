from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

from shared.logging import get_logger

logger = get_logger(__name__)


@contextmanager
def llm_span(provider: str, model: str = "unknown") -> Iterator[None]:
    from ai_platform.config.settings import get_settings

    settings = get_settings()
    if not settings.otel_enabled:
        yield
        return

    try:
        from opentelemetry import trace

        tracer = trace.get_tracer("ai_platform.llm")
        with tracer.start_as_current_span(
            "llm.invoke",
            attributes={"llm.provider": provider, "llm.model": model},
        ):
            yield
    except Exception as exc:
        logger.debug("llm_span_skipped", error=str(exc))
        yield


@contextmanager
def agent_span(agent_name: str, session_id: str = "") -> Iterator[None]:
    from ai_platform.config.settings import get_settings

    settings = get_settings()
    if not settings.otel_enabled:
        yield
        return

    try:
        from opentelemetry import trace

        tracer = trace.get_tracer("ai_platform.agents")
        attrs: dict[str, Any] = {"agent.name": agent_name}
        if session_id:
            attrs["session.id"] = session_id
        with tracer.start_as_current_span("agent.run", attributes=attrs):
            yield
    except Exception as exc:
        logger.debug("agent_span_skipped", error=str(exc))
        yield
