from __future__ import annotations

class OllamaProvider:
    async def ainvoke(self, prompt: str, tools: list | None = None) -> str:
        return f"[ollama] {prompt[:80]}"
