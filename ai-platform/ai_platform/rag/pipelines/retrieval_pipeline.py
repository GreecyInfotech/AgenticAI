from __future__ import annotations

from ai_platform.rag.retriever.retriever import RetrievalRequest, RetrievalResponse, RetrievedChunk

_KNOWLEDGE = [
    {"id": "k1", "content": "Minimum order quantity is 10 units for wholesale distributors.", "tags": ["order"]},
    {"id": "k2", "content": "Credit terms: Net 30 for approved distributors.", "tags": ["credit"]},
    {"id": "k3", "content": "Free shipping on orders over $500.", "tags": ["promotion", "shipment"]},
]


class HybridRetriever:
    async def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        query = request.query.lower()
        scored = []
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
