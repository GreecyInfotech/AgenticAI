"""Vector store client — ChromaDB with hash embedding fallback."""

from __future__ import annotations

import hashlib
from typing import Any

import chromadb

from eaap_platform.config import get_settings


class VectorStoreClient:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self._collection = self._client.get_or_create_collection(settings.chroma_collection)

    def _embed(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode()).digest()
        return [((digest[i % len(digest)] / 255.0) * 2 - 1) for i in range(768)]

    def upsert(self, ids: list[str], texts: list[str], metadatas: list[dict[str, Any]]) -> int:
        embeddings = [self._embed(t) for t in texts]
        self._collection.upsert(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)
        return len(ids)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        result = self._collection.query(query_embeddings=[self._embed(query)], n_results=top_k)
        items: list[dict[str, Any]] = []
        for i, doc_id in enumerate(result["ids"][0]):
            distance = result["distances"][0][i] if result.get("distances") else 0.0
            items.append(
                {
                    "id": doc_id,
                    "content": result["documents"][0][i],
                    "score": round(1 - distance, 4),
                    "metadata": result["metadatas"][0][i] if result.get("metadatas") else {},
                }
            )
        return items
