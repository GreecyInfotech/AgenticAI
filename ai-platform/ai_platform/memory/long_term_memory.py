from __future__ import annotations

from ai_platform.infrastructure.database import get_pool
from ai_platform.infrastructure.redis_client import get_redis
from shared.logging import get_logger

logger = get_logger(__name__)

_ltm_cache: dict[str, str] = {}


class LongTermMemory:
    def _cache_key(self, customer_id: str, key: str) -> str:
        return f"ltm:{customer_id}:{key}"

    async def store(self, customer_id: str, key: str, value: str) -> None:
        redis_key = self._cache_key(customer_id, key)
        client = get_redis()
        if client is not None:
            await client.set(redis_key, value)
        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO long_term_memory (customer_id, memory_key, memory_value)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (customer_id, memory_key) DO UPDATE
                    SET memory_value = EXCLUDED.memory_value, updated_at = NOW()
                    """,
                    customer_id,
                    key,
                    value,
                )
        else:
            _ltm_cache[redis_key] = value
        logger.info("long_term_memory_stored", customer_id=customer_id, key=key)

    async def recall(self, customer_id: str, key: str) -> str | None:
        redis_key = self._cache_key(customer_id, key)
        client = get_redis()
        if client is not None:
            value = await client.get(redis_key)
            if value:
                return value
        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT memory_value FROM long_term_memory WHERE customer_id = $1 AND memory_key = $2",
                    customer_id,
                    key,
                )
                if row:
                    return str(row["memory_value"])
        return _ltm_cache.get(redis_key)
