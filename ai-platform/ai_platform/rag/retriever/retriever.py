from __future__ import annotations

from ai_platform.config.settings import get_settings
from ai_platform.rag.embeddings.embedder import embed_text
from ai_platform.rag.pipelines.retrieval_pipeline import HybridRetriever
from ai_platform.rag.schemas import RetrievalRequest, RetrievalResponse, RetrievedChunk
from ai_platform.rag.vector_store.qdrant_store import QdrantVectorStore
from shared.logging import get_logger

logger = get_logger(__name__)

_DEFAULT_DOCS = [
    {"id": "k1", "content": "Minimum order quantity is 10 units for wholesale distributors.", "tags": ["order"]},
    {"id": "k2", "content": "Credit terms: Net 30 for approved distributors.", "tags": ["credit"]},
    {"id": "k3", "content": "Free shipping on orders over $500.", "tags": ["promotion", "shipment"]},
    {"id": "k4", "content": "Returns accepted within 30 days for unopened merchandise.", "tags": ["policy"]},
    {"id": "k5", "content": "Volume discounts apply at 100+ unit orders.", "tags": ["pricing", "promotion"]},
]


class KnowledgeRetriever:
    def __init__(self) -> None:
        self._hybrid = HybridRetriever()
        self._store = QdrantVectorStore()

    async def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        vector = await embed_text(request.query)
        vector_hits = await self._store.search(request.collection, vector, top_k=request.top_k)
        if vector_hits:
            chunks = [
                RetrievedChunk(
                    id=hit["id"],
                    content=str(hit["payload"].get("content", "")),
                    score=float(hit["score"]),
                    metadata={"tags": hit["payload"].get("tags", [])},
                )
                for hit in vector_hits
                if hit["payload"].get("content")
            ]
            if chunks:
                from ai_platform.telemetry.metrics import record_rag_retrieval

                record_rag_retrieval("vector")
                return RetrievalResponse(query=request.query, chunks=chunks)

        from ai_platform.telemetry.metrics import record_rag_retrieval

        record_rag_retrieval("keyword")
        return await self._hybrid.retrieve(request)


async def bootstrap_knowledge_base() -> None:
    settings = get_settings()
    if not settings.rag_bootstrap_on_startup:
        return

    store = QdrantVectorStore()
    collection = settings.qdrant_collection
    sample_vector = await embed_text("bootstrap")
    await store.ensure_collection(collection, vector_size=len(sample_vector))

    for doc in _DEFAULT_DOCS:
        vector = await embed_text(doc["content"])
        await store.upsert(
            collection=collection,
            doc_id=doc["id"],
            vector=vector,
            payload={"content": doc["content"], "tags": doc["tags"]},
        )
    logger.info("rag_knowledge_bootstrapped", documents=len(_DEFAULT_DOCS), collection=collection)
