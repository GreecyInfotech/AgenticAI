from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import asyncpg
from tenacity import retry, stop_after_attempt, wait_exponential

from ai_platform.config.settings import get_settings
from shared.logging import get_logger

logger = get_logger(__name__)

_pool: asyncpg.Pool | None = None


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4), reraise=True)
async def init_db_pool() -> asyncpg.Pool | None:
    global _pool
    settings = get_settings()
    try:
        ssl = "require" if settings.postgres_ssl else None
        _pool = await asyncpg.create_pool(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_db,
            min_size=settings.postgres_min_pool,
            max_size=settings.postgres_max_pool,
            command_timeout=settings.postgres_command_timeout,
            ssl=ssl,
        )
        async with _pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        logger.info("postgres_pool_created", host=settings.postgres_host, database=settings.postgres_db)
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
        logger.info("postgres_pool_closed")


def get_pool() -> asyncpg.Pool | None:
    return _pool


@asynccontextmanager
async def acquire_connection() -> AsyncIterator[asyncpg.Connection]:
    pool = get_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL pool is not initialized")
    async with pool.acquire() as conn:
        yield conn


@asynccontextmanager
async def run_transaction() -> AsyncIterator[asyncpg.Connection]:
    pool = get_pool()
    if pool is None:
        raise RuntimeError("PostgreSQL pool is not initialized")
    async with pool.acquire() as conn:
        async with conn.transaction():
            yield conn


async def execute_query(query: str, *args: Any) -> list[asyncpg.Record]:
    async with acquire_connection() as conn:
        return await conn.fetch(query, *args)


async def check_db_health() -> dict[str, Any]:
    pool = get_pool()
    if pool is None:
        return {"status": "DOWN", "detail": "pool not initialized"}
    try:
        async with pool.acquire() as conn:
            version = await conn.fetchval("SELECT version()")
            size = pool.get_size()
        return {"status": "UP", "pool_size": size, "server": str(version).split(",")[0]}
    except Exception as exc:
        return {"status": "DOWN", "detail": str(exc)}
