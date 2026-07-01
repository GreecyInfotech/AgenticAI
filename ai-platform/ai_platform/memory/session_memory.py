from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

from ai_platform.config.settings import get_settings
from ai_platform.infrastructure.redis_client import get_redis
from shared.logging import get_logger

logger = get_logger(__name__)

_memory_store: dict[str, list[dict[str, Any]]] = defaultdict(list)


class InMemorySessionBackend:
    def __init__(self, session_id: str) -> None:
        self.session_id = session_id

    async def get_messages(self) -> list[dict[str, Any]]:
        return list(_memory_store[self.session_id])

    async def add_message(self, role: str, content: str) -> None:
        _memory_store[self.session_id].append({"role": role, "content": content})


class RedisSessionBackend:
    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        self._key = f"session:{session_id}:messages"
        self._ttl = get_settings().memory_session_ttl_seconds

    async def get_messages(self) -> list[dict[str, Any]]:
        client = get_redis()
        if client is None:
            return await InMemorySessionBackend(self.session_id).get_messages()
        raw = await client.get(self._key)
        if not raw:
            return []
        return json.loads(raw)

    async def add_message(self, role: str, content: str) -> None:
        client = get_redis()
        messages = await self.get_messages()
        messages.append({"role": role, "content": content})
        if client is None:
            await InMemorySessionBackend(self.session_id).add_message(role, content)
            return
        await client.set(self._key, json.dumps(messages), ex=self._ttl)


class SessionMemory:
    """Session memory facade — Redis when available, in-process fallback."""

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        self._backend: InMemorySessionBackend | RedisSessionBackend = (
            RedisSessionBackend(session_id) if get_redis() is not None else InMemorySessionBackend(session_id)
        )

    async def get_messages(self) -> list[dict[str, Any]]:
        return await self._backend.get_messages()

    async def add_message(self, role: str, content: str) -> None:
        await self._backend.add_message(role, content)
        logger.debug("session_message_added", session_id=self.session_id, role=role)
