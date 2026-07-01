from __future__ import annotations

import hashlib
import math

from ai_platform.config.settings import get_settings
from shared.logging import get_logger

logger = get_logger(__name__)

_VECTOR_SIZE = 384


def _hash_embed(text: str) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [digest[i % len(digest)] / 255.0 for i in range(_VECTOR_SIZE)]
    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


async def embed_text(text: str) -> list[float]:
    settings = get_settings()
    if settings.openai_api_key:
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.embeddings.create(
                model=settings.openai_embedding_model,
                input=text,
            )
            return list(response.data[0].embedding)
        except Exception as exc:
            logger.warning("openai_embedding_failed", error=str(exc))
    return _hash_embed(text)


async def embed_batch(texts: list[str]) -> list[list[float]]:
    return [await embed_text(text) for text in texts]
