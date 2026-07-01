from __future__ import annotations

from ai_platform.infrastructure.database import get_pool
from shared.logging import get_logger

logger = get_logger(__name__)

_summary_cache: dict[str, str] = {}


class PostgresMemory:
    async def save_summary(self, session_id: str, customer_id: str, summary: str) -> None:
        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO conversation_summaries (session_id, customer_id, summary)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (session_id) DO UPDATE
                    SET summary = EXCLUDED.summary, customer_id = EXCLUDED.customer_id, updated_at = NOW()
                    """,
                    session_id,
                    customer_id,
                    summary,
                )
        else:
            _summary_cache[session_id] = summary
        logger.info("conversation_summary_saved", session_id=session_id)

    async def load_summary(self, session_id: str) -> str | None:
        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT summary FROM conversation_summaries WHERE session_id = $1",
                    session_id,
                )
                if row:
                    return str(row["summary"])
        return _summary_cache.get(session_id)
