from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ai_platform.config.settings import get_settings
from shared.logging import get_logger

logger = get_logger(__name__)


class OllamaProvider:
    provider_name = "ollama"

    def __init__(self) -> None:
        settings = get_settings()
        self.model = settings.ollama_model
        self._base_url = settings.ollama_base_url.rstrip("/")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4), reraise=True)
    async def ainvoke(self, prompt: str, tools: list[dict[str, Any]] | None = None) -> str:
        _ = tools
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        async with httpx.AsyncClient(timeout=get_settings().llm_timeout_seconds) as client:
            response = await client.post(f"{self._base_url}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()
            return str(data.get("response", ""))
