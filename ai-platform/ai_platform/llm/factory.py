from __future__ import annotations

import time
from typing import Any, Protocol

from shared.logging import get_logger
from shared.security.prompt_injection import is_prompt_injection

from ai_platform.llm.cost_tracker import estimate_cost, track_usage
from ai_platform.llm.guardrails import validate_input, validate_output
from ai_platform.telemetry.metrics import record_llm_request
from ai_platform.telemetry.tracing import llm_span

logger = get_logger(__name__)


class LLMProvider(Protocol):
    provider_name: str

    async def ainvoke(self, prompt: str, tools: list[dict[str, Any]] | None = None) -> str: ...


class InstrumentedLLM:
    """Wraps a provider with guardrails, metrics, tracing, and cost tracking."""

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider
        self.provider_name = provider.provider_name

    async def ainvoke(self, prompt: str, tools: list[dict[str, Any]] | None = None) -> str:
        validate_input(prompt)
        start = time.perf_counter()
        try:
            with llm_span(self.provider_name, model=getattr(self._provider, "model", "unknown")):
                response = await self._provider.ainvoke(prompt, tools=tools)
        except Exception as exc:
            record_llm_request(self.provider_name, success=False, latency=time.perf_counter() - start)
            logger.error("llm_invoke_failed", provider=self.provider_name, error=str(exc))
            raise

        latency = time.perf_counter() - start
        safe_response = validate_output(response)
        tokens = estimate_cost(prompt, safe_response, self.provider_name)
        track_usage(self.provider_name, tokens["total_tokens"], tokens["estimated_cost_usd"])
        record_llm_request(self.provider_name, success=True, latency=latency)
        return safe_response


class MockLLM:
    provider_name = "mock"
    model = "mock"

    async def ainvoke(self, prompt: str, tools: list[dict[str, Any]] | None = None) -> str:
        return f"[mock-response] Processed request ({len(prompt)} chars)"


def get_llm(task: str = "default") -> LLMProvider:
    from ai_platform.llm.router import resolve_provider

    provider = resolve_provider(task)
    return InstrumentedLLM(provider)
