from __future__ import annotations

from ai_platform.memory.session_memory import SessionMemory


class CreditAgentMemory:
    def __init__(self, session_id: str) -> None:
        self._memory = SessionMemory(session_id)

    async def load(self) -> list[dict]:
        return await self._memory.get_messages()

    async def save(self, role: str, content: str) -> None:
        await self._memory.add_message(role, content)
