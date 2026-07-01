from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from ai_platform.infrastructure.database import close_db_pool, init_db_pool
from ai_platform.infrastructure.redis_client import close_redis, init_redis
from shared.logging import configure_logging, get_logger
from shared.messaging import close_kafka_producer, init_kafka_producer

logger = get_logger(__name__)

_STARTUP_TIMEOUT = 5.0


async def _safe_init(name: str, coro) -> None:
    try:
        await asyncio.wait_for(coro, timeout=_STARTUP_TIMEOUT)
    except TimeoutError:
        logger.warning(f"{name}_init_timeout")
    except Exception as exc:
        logger.warning(f"{name}_init_failed", error=str(exc))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    from ai_platform.config.settings import get_settings

    settings = get_settings()
    configure_logging(settings.log_level)
    logger.info("ai_platform_starting", env=settings.app_env)

    await _safe_init("postgres", init_db_pool())
    await _safe_init("redis", init_redis())
    await _safe_init("kafka", init_kafka_producer())
    app.state.ready = True
    logger.info("ai_platform_ready")

    yield

    app.state.ready = False
    await close_kafka_producer()
    await close_redis()
    await close_db_pool()
    logger.info("ai_platform_stopped")
