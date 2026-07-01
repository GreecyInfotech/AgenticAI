from __future__ import annotations

from typing import Any

import asyncpg

from ai_platform.config.settings import get_settings
from shared.logging import get_logger

logger = get_logger(__name__)

_pool: asyncpg.Pool | None = None


async def init_db_pool() -> asyncpg.Pool | None:
    global _pool
    settings = get_settings()
    try:
        _pool = await asyncpg.create_pool(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_db,
            min_size=2,
            max_size=10,
            command_timeout=30,
        )
        logger.info("postgres_pool_created", host=settings.postgres_host)
        return _pool
    except Exception as exc:
        logger.warning("postgres_unavailable", error=str(exc))
        _pool = None
        return None


async def close_db_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool | None:
    return _pool


async def check_db_health() -> dict[str, Any]:
    pool = get_pool()
    if pool is None:
        return {"status": "DOWN", "detail": "pool not initialized"}
    try:
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return {"status": "UP"}
    except Exception as exc:
        return {"status": "DOWN", "detail": str(exc)}
