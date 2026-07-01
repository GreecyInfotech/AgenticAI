from __future__ import annotations

import time
from typing import Any

from ai_platform.config.settings import get_settings
from shared.logging import get_logger

logger = get_logger(__name__)

_client: Any | None = None


async def init_qdrant() -> Any | None:
    global _client
    settings = get_settings()
    if not settings.qdrant_enabled:
        logger.info("qdrant_disabled")
        return None
    try:
        from qdrant_client import AsyncQdrantClient

        kwargs: dict[str, Any] = {
            "host": settings.qdrant_host,
            "port": settings.qdrant_port,
            "timeout": 5,
            "https": settings.qdrant_https,
        }
        if settings.qdrant_api_key:
            kwargs["api_key"] = settings.qdrant_api_key

        _client = AsyncQdrantClient(**kwargs)
        await _client.get_collections()
        logger.info("qdrant_connected", host=settings.qdrant_host, port=settings.qdrant_port)
        return _client
    except Exception as exc:
        logger.warning("qdrant_unavailable", error=str(exc))
        _client = None
        return None


async def close_qdrant() -> None:
    global _client
    if _client is not None:
        await _client.close()
        _client = None
        logger.info("qdrant_closed")


def get_qdrant() -> Any | None:
    return _client


async def ensure_collection(collection: str, vector_size: int) -> None:
    client = get_qdrant()
    if client is None:
        return
    from qdrant_client.models import Distance, VectorParams

    collections = await client.get_collections()
    names = {item.name for item in collections.collections}
    if collection not in names:
        await client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        logger.info("qdrant_collection_created", collection=collection)


async def check_qdrant_health() -> dict[str, Any]:
    settings = get_settings()
    if not settings.qdrant_enabled:
        return {"status": "DISABLED"}
    client = get_qdrant()
    if client is None:
        return {"status": "DOWN", "detail": "client not initialized"}
    try:
        start = time.perf_counter()
        collections = await client.get_collections()
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        return {
            "status": "UP",
            "latency_ms": latency_ms,
            "collections": len(collections.collections),
        }
    except Exception as exc:
        return {"status": "DOWN", "detail": str(exc)}
