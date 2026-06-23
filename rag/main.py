"""RAG service — document ingestion and semantic search."""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, Field

from eaap_platform.app_factory import create_service_app
from vector_store.client import VectorStoreClient

app = create_service_app("RAG Service", "1.0.0")
_store = VectorStoreClient()


class IngestRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1)
    metadatas: list[dict[str, Any]] = Field(default_factory=list)


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = 5


@app.post("/ingest")
async def ingest(request: IngestRequest) -> dict[str, Any]:
    ids = [str(uuid.uuid4()) for _ in request.texts]
    metas = request.metadatas or [{} for _ in request.texts]
    if len(metas) != len(request.texts):
        raise HTTPException(status_code=400, detail="metadatas length must match texts")
    count = _store.upsert(ids, request.texts, metas)
    return {"ingested": count, "ids": ids}


@app.post("/search")
async def search(request: SearchRequest) -> dict[str, Any]:
    return {"results": _store.search(request.query, request.top_k)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
