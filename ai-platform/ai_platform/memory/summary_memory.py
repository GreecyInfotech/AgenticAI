from __future__ import annotations

class SummaryMemory:
    async def summarize(self, messages: list[dict]) -> str:
        if not messages:
            return ""
        return f"Summary of {len(messages)} messages"
