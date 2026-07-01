from __future__ import annotations

from ai_platform.memory.session_memory import SessionMemory

class LongTermMemory:
    async def store(self, customer_id: str, key: str, value: str) -> None:
        pass

    async def recall(self, customer_id: str, key: str) -> str | None:
        return None
