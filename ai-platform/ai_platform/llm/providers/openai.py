from __future__ import annotations

from ai_platform.config.settings import get_settings
from ai_platform.llm.factory import LLMProvider


class OpenAIProvider:
  async def ainvoke(self, prompt: str, tools: list | None = None) -> str:
    settings = get_settings()
    try:
      from langchain_openai import ChatOpenAI
      from langchain_core.messages import HumanMessage

      llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)
      result = await llm.ainvoke([HumanMessage(content=prompt)])
      return str(result.content)
    except Exception as exc:
      return f"[openai-fallback] {exc}"
