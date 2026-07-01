from __future__ import annotations

from typing import Any

import redis.asyncio as aioredis

from ai_platform.config.settings import get_settings
from shared.logging import get_logger

logger = get_logger(__name__)

_client: aioredis.Redis | None = None


async def init_redis() -> aioredis.Redis | None:
    global _client
    settings = get_settings()
    try:
        _client = aioredis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True,
            socket_connect_timeout=2,
        )
        await _client.ping()
        logger.info("redis_connected", host=settings.redis_host)
        return _client
    except Exception as exc:
        logger.warning("redis_unavailable", error=str(exc))
        _client = None
        return None


async def close_redis() -> None:
    global _client
    if _client is not None:
        await _client.close()
        _client = None


def get_redis() -> aioredis.Redis | None:
    return _client


async def check_redis_health() -> dict[str, Any]:
    client = get_redis()
    if client is None:
        return {"status": "DOWN", "detail": "client not initialized"}
    try:
        await client.ping()
        return {"status": "UP"}
    except Exception as exc:
        return {"status": "DOWN", "detail": str(exc)}
