from __future__ import annotations

from ai_platform.config.settings import get_settings
from ai_platform.llm.factory import LLMProvider, MockLLM


def resolve_provider(task: str = "default") -> LLMProvider:
    settings = get_settings()
    provider = settings.llm_provider.lower()

    if provider == "openai" and settings.openai_api_key:
        from ai_platform.llm.providers.openai import OpenAIProvider

        return OpenAIProvider()
    if provider == "ollama":
        from ai_platform.llm.providers.ollama import OllamaProvider

        return OllamaProvider()
    if provider == "azure_openai" and settings.openai_api_key:
        from ai_platform.llm.providers.azure_openai import AzureOpenAIProvider

        return AzureOpenAIProvider()

    _ = task
    return MockLLM()


def get_provider_name() -> str:
    return get_settings().llm_provider
