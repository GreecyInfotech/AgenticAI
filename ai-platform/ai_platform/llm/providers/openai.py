from __future__ import annotations

from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential

from ai_platform.config.settings import get_settings
from ai_platform.llm.factory import LLMProvider
from shared.logging import get_logger

logger = get_logger(__name__)


class OpenAIProvider:
    provider_name = "openai"

    def __init__(self) -> None:
        settings = get_settings()
        self.model = settings.openai_model
        self._api_key = settings.openai_api_key
        self._max_retries = settings.llm_max_retries

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4), reraise=True)
    async def ainvoke(self, prompt: str, tools: list[dict[str, Any]] | None = None) -> str:
        from langchain_core.messages import HumanMessage
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model=self.model,
            api_key=self._api_key,
            timeout=get_settings().llm_timeout_seconds,
        )
        if tools:
            llm = llm.bind_tools(tools)
        result = await llm.ainvoke([HumanMessage(content=prompt)])
        return str(result.content)
