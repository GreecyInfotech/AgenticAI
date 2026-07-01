from __future__ import annotations

from typing import Any

from ai_platform.config.settings import get_settings
from ai_platform.llm.providers.openai import OpenAIProvider


class AzureOpenAIProvider(OpenAIProvider):
    provider_name = "azure_openai"

    def __init__(self) -> None:
        super().__init__()
        settings = get_settings()
        self._azure_endpoint = getattr(settings, "azure_openai_endpoint", "")

    async def ainvoke(self, prompt: str, tools: list[dict[str, Any]] | None = None) -> str:
        if not self._azure_endpoint:
            return await super().ainvoke(prompt, tools=tools)
        from langchain_core.messages import HumanMessage
        from langchain_openai import AzureChatOpenAI

        llm = AzureChatOpenAI(
            azure_endpoint=self._azure_endpoint,
            api_key=self._api_key,
            azure_deployment=self.model,
            timeout=get_settings().llm_timeout_seconds,
        )
        result = await llm.ainvoke([HumanMessage(content=prompt)])
        return str(result.content)
