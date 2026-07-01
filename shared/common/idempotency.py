from __future__ import annotations

import json
from typing import Any

from shared.exceptions import IdempotencyConflictError


class IdempotencyStore:
    """In-memory idempotency store; production deployments should use Redis."""

    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    async def get(self, key: str) -> dict[str, Any] | None:
        return self._store.get(key)

    async def set(self, key: str, value: dict[str, Any]) -> None:
        if key in self._store and self._store[key].get("status") == "processing":
            raise IdempotencyConflictError(key)
        self._store[key] = value

    async def complete(self, key: str, response: dict[str, Any]) -> None:
        self._store[key] = {"status": "completed", "response": response}

    def serialize_response(self, response: Any) -> dict[str, Any]:
        if hasattr(response, "model_dump"):
            return response.model_dump()
        if isinstance(response, dict):
            return response
        return {"result": json.loads(json.dumps(response, default=str))}


idempotency_store = IdempotencyStore()
