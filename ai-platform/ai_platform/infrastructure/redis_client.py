from __future__ import annotations

import json
import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import redis.asyncio as aioredis
from tenacity import retry, stop_after_attempt, wait_exponential

from ai_platform.config.settings import get_settings
from shared.logging import get_logger

logger = get_logger(__name__)

_client: aioredis.Redis | None = None


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4), reraise=True)
async def init_redis() -> aioredis.Redis | None:
    global _client
    settings = get_settings()
    try:
        _client = aioredis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password or None,
            db=settings.redis_db,
            decode_responses=True,
            socket_connect_timeout=settings.redis_socket_timeout,
            socket_timeout=settings.redis_socket_timeout,
            ssl=settings.redis_ssl,
            health_check_interval=30,
        )
        await _client.ping()
        logger.info("redis_connected", host=settings.redis_host, db=settings.redis_db)
        return _client
    except Exception as exc:
        logger.warning("redis_unavailable", error=str(exc))
        _client = None
        return None


async def close_redis() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
        logger.info("redis_closed")


def get_redis() -> aioredis.Redis | None:
    return _client


async def cache_get(key: str) -> str | None:
    client = get_redis()
    if client is None:
        return None
    return await client.get(key)


async def cache_set(key: str, value: str, ttl_seconds: int = 300) -> None:
    client = get_redis()
    if client is None:
        return
    await client.set(key, value, ex=ttl_seconds)


async def cache_get_json(key: str) -> Any | None:
    raw = await cache_get(key)
    if raw is None:
        return None
    return json.loads(raw)


async def cache_set_json(key: str, value: Any, ttl_seconds: int = 300) -> None:
    await cache_set(key, json.dumps(value), ttl_seconds=ttl_seconds)


@asynccontextmanager
async def distributed_lock(name: str, ttl_seconds: int = 30) -> AsyncIterator[bool]:
    """Best-effort Redis lock using SET NX. Yields True if lock acquired."""
    client = get_redis()
    if client is None:
        yield True
        return

    token = str(uuid.uuid4())
    acquired = await client.set(f"lock:{name}", token, nx=True, ex=ttl_seconds)
    try:
        yield bool(acquired)
    finally:
        if acquired:
            current = await client.get(f"lock:{name}")
            if current == token:
                await client.delete(f"lock:{name}")


async def check_redis_health() -> dict[str, Any]:
    client = get_redis()
    if client is None:
        return {"status": "DOWN", "detail": "client not initialized"}
    try:
        start = time.perf_counter()
        await client.ping()
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        info = await client.info(section="memory")
        return {
            "status": "UP",
            "latency_ms": latency_ms,
            "used_memory_human": info.get("used_memory_human", "unknown"),
        }
    except Exception as exc:
        return {"status": "DOWN", "detail": str(exc)}
