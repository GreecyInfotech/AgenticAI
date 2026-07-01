from __future__ import annotations

import json

from ai_platform.config.settings import get_settings
from ai_platform.infrastructure.redis_client import get_redis
from shared.logging import get_logger

logger = get_logger(__name__)

_memory_kv: dict[str, str] = {}


class RedisMemory:
    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        self._prefix = f"session:{session_id}:kv"
        self._ttl = get_settings().memory_session_ttl_seconds

    async def get(self, key: str) -> str | None:
        full_key = f"{self._prefix}:{key}"
        client = get_redis()
        if client is None:
            return _memory_kv.get(full_key)
        return await client.get(full_key)

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        full_key = f"{self._prefix}:{key}"
        expire = ttl or self._ttl
        client = get_redis()
        if client is None:
            _memory_kv[full_key] = value
            return
        await client.set(full_key, value, ex=expire)
        logger.debug("redis_memory_set", session_id=self.session_id, key=key)
