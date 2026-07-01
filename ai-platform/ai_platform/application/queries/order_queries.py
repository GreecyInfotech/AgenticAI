from __future__ import annotations

from pydantic import BaseModel, Field


class GetOrderQuery(BaseModel):
    order_id: str


class ListOrdersQuery(BaseModel):
    customer_id: str | None = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
