from __future__ import annotations

from pydantic import BaseModel, Field


class OrderItemInput(BaseModel):
    sku: str
    quantity: int = Field(ge=1)


class PlaceOrderCommand(BaseModel):
    customer_id: str
    items: list[OrderItemInput]
