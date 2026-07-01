from __future__ import annotations

import math
from typing import Any

from ai_platform.infrastructure.qdrant_client import get_qdrant
from shared.logging import get_logger

logger = get_logger(__name__)

_memory_vectors: dict[str, list[dict[str, Any]]] = {}


class QdrantVectorStore:
    async def ensure_collection(self, collection: str, vector_size: int) -> None:
        client = get_qdrant()
        if client is None:
            _memory_vectors.setdefault(collection, [])
            return
        from qdrant_client.models import Distance, VectorParams

        collections = await client.get_collections()
        names = {c.name for c in collections.collections}
        if collection not in names:
            await client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            logger.info("qdrant_collection_created", collection=collection)

    async def upsert(self, collection: str, doc_id: str, vector: list[float], payload: dict) -> None:
        client = get_qdrant()
        if client is None:
            bucket = [item for item in _memory_vectors.get(collection, []) if item["id"] != doc_id]
            bucket.append({"id": doc_id, "vector": vector, "payload": payload})
            _memory_vectors[collection] = bucket
            return
        from qdrant_client.models import PointStruct

        await client.upsert(
            collection_name=collection,
            points=[PointStruct(id=doc_id, vector=vector, payload=payload)],
        )

    async def search(self, collection: str, vector: list[float], top_k: int = 5) -> list[dict]:
        client = get_qdrant()
        if client is None:
            return self._memory_search(collection, vector, top_k)
        hits = await client.search(collection_name=collection, query_vector=vector, limit=top_k)
        return [
            {
                "id": str(hit.id),
                "score": float(hit.score),
                "payload": hit.payload or {},
            }
            for hit in hits
        ]

    def _memory_search(self, collection: str, vector: list[float], top_k: int) -> list[dict]:
        items = _memory_vectors.get(collection, [])
        scored: list[tuple[float, dict[str, Any]]] = []
        for item in items:
            score = _cosine_similarity(vector, item["vector"])
            scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"id": item["id"], "score": score, "payload": item["payload"]}
            for score, item in scored[:top_k]
        ]


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    size = min(len(a), len(b))
    if size == 0:
        return 0.0
    dot = sum(a[i] * b[i] for i in range(size))
    norm_a = math.sqrt(sum(a[i] * a[i] for i in range(size))) or 1.0
    norm_b = math.sqrt(sum(b[i] * b[i] for i in range(size))) or 1.0
    return dot / (norm_a * norm_b)
