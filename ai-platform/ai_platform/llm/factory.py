from __future__ import annotations

from typing import Any, Protocol


class LLMProvider(Protocol):
    async def ainvoke(self, prompt: str, tools: list[dict[str, Any]] | None = None) -> str: ...


class MockLLM:
    async def ainvoke(self, prompt: str, tools: list[dict[str, Any]] | None = None) -> str:
        return f"[mock-response] Processed request ({len(prompt)} chars)"


def get_llm() -> LLMProvider:
    from ai_platform.config.settings import get_settings

    settings = get_settings()
    if settings.llm_provider == "openai" and settings.openai_api_key:
        from ai_platform.llm.providers.openai import OpenAIProvider

        return OpenAIProvider()
    return MockLLM()
