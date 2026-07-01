from __future__ import annotations

from pydantic import BaseModel, Field


class GetCustomerQuery(BaseModel):
    customer_id: str


class ListCustomersQuery(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
