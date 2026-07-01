from __future__ import annotations

class RedisMemory:
    def __init__(self, session_id: str) -> None:
        self.session_id = session_id

    async def get(self, key: str) -> str | None:
        return None

    async def set(self, key: str, value: str, ttl: int = 3600) -> None:
        pass
