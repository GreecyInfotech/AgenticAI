from __future__ import annotations

class AnthropicProvider:
    async def ainvoke(self, prompt: str, tools: list | None = None) -> str:
        return f"[anthropic] {prompt[:80]}"
