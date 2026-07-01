from __future__ import annotations

class QdrantVectorStore:
    async def upsert(self, collection: str, doc_id: str, vector: list[float], payload: dict) -> None:
        pass

    async def search(self, collection: str, vector: list[float], top_k: int = 5) -> list[dict]:
        return []
