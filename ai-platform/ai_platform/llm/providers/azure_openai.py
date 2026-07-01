from __future__ import annotations

class AzureOpenAIProvider:
    async def ainvoke(self, prompt: str, tools: list | None = None) -> str:
        return f"[azure-openai] {prompt[:80]}"
