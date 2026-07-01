from __future__ import annotations

from pydantic import BaseModel, Field


class InventoryResponseDTO(BaseModel):
    sku: str
    available: int
    warehouse: str


class ReserveInventoryRequestDTO(BaseModel):
    quantity: int = Field(ge=1)
    order_id: str


class ReserveInventoryResponseDTO(BaseModel):
    sku: str
    reserved: int
    order_id: str
    remaining: int
