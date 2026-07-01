from __future__ import annotations

class PostgresMemory:
    async def save_summary(self, session_id: str, summary: str) -> None:
        pass

    async def load_summary(self, session_id: str) -> str | None:
        return None
