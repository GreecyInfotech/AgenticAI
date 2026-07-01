from __future__ import annotations

class VertexAIProvider:
    async def ainvoke(self, prompt: str, tools: list | None = None) -> str:
        return f"[vertex-ai] {prompt[:80]}"
