from __future__ import annotations

from collections import defaultdict
from typing import Any


class SessionMemory:
    _store: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id

    async def get_messages(self) -> list[dict[str, Any]]:
        return list(self._store[self.session_id])

    async def add_message(self, role: str, content: str) -> None:
        self._store[self.session_id].append({"role": role, "content": content})
