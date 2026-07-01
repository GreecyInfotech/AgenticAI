from __future__ import annotations

from pydantic import BaseModel, Field


class ListProductsQuery(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class GetInventoryQuery(BaseModel):
    sku: str
