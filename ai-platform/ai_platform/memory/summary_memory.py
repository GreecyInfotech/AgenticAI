from __future__ import annotations

from ai_platform.config.settings import get_settings
from ai_platform.memory.postgres_memory import PostgresMemory
from shared.logging import get_logger

logger = get_logger(__name__)


class SummaryMemory:
    def __init__(self) -> None:
        self._postgres = PostgresMemory()
        self._threshold = get_settings().memory_summary_threshold

    async def summarize(self, messages: list[dict], session_id: str = "", customer_id: str = "") -> str:
        if not messages:
            return ""
        if len(messages) <= self._threshold:
            return "\n".join(f"{m['role']}: {m['content']}" for m in messages[-self._threshold :])

        if session_id:
            existing = await self._postgres.load_summary(session_id)
            if existing:
                return existing

        summary = self._build_summary(messages)
        if session_id and customer_id:
            await self._postgres.save_summary(session_id, customer_id, summary)
        return summary

    def _build_summary(self, messages: list[dict]) -> str:
        recent = messages[-self._threshold :]
        lines = [f"{m['role']}: {m['content'][:200]}" for m in recent]
        return f"Summary of {len(messages)} messages.\n" + "\n".join(lines)
