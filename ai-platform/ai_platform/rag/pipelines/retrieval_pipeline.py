from __future__ import annotations

from ai_platform.rag.schemas import RetrievalRequest, RetrievalResponse, RetrievedChunk

_KNOWLEDGE = [
    {"id": "k1", "content": "Minimum order quantity is 10 units for wholesale distributors.", "tags": ["order"]},
    {"id": "k2", "content": "Credit terms: Net 30 for approved distributors.", "tags": ["credit"]},
    {"id": "k3", "content": "Free shipping on orders over $500.", "tags": ["promotion", "shipment"]},
    {"id": "k4", "content": "Returns accepted within 30 days for unopened merchandise.", "tags": ["policy"]},
    {"id": "k5", "content": "Volume discounts apply at 100+ unit orders.", "tags": ["pricing", "promotion"]},
]


class HybridRetriever:
    async def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        query = request.query.lower()
        scored: list[tuple[int, dict]] = []
        for doc in _KNOWLEDGE:
            score = sum(1 for word in query.split() if word in doc["content"].lower())
            if score > 0:
                scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        chunks = [
            RetrievedChunk(id=doc["id"], content=doc["content"], score=float(score), metadata={"tags": doc["tags"]})
            for score, doc in scored[: request.top_k]
        ]
        return RetrievalResponse(query=request.query, chunks=chunks)
