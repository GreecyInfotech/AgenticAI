from __future__ import annotations

from pydantic import BaseModel, Field


class OrderItemDTO(BaseModel):
    sku: str
    quantity: int
    unit_price: float
    line_total: float


class OrderResponseDTO(BaseModel):
    order_id: str
    customer_id: str
    status: str
    total: float
    items: list[OrderItemDTO] | list[dict] = Field(default_factory=list)


class CreateOrderRequestDTO(BaseModel):
    customer_id: str
    items: list[dict]
