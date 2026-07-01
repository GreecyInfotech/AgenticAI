from __future__ import annotations

from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    collection: str = "distributor_knowledge"


class RetrievedChunk(BaseModel):
    id: str
    content: str
    score: float
    metadata: dict = Field(default_factory=dict)


class RetrievalResponse(BaseModel):
    query: str
    chunks: list[RetrievedChunk]
