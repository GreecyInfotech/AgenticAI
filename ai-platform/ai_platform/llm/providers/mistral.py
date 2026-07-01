from __future__ import annotations

class MistralProvider:
    async def ainvoke(self, prompt: str, tools: list | None = None) -> str:
        return f"[mistral] {prompt[:80]}"
