from __future__ import annotations

class BedrockProvider:
    async def ainvoke(self, prompt: str, tools: list | None = None) -> str:
        return f"[bedrock] {prompt[:80]}"
