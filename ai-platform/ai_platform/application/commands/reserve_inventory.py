from __future__ import annotations

from pydantic import BaseModel, Field


class ReserveInventoryCommand(BaseModel):
    sku: str
    quantity: int = Field(ge=1)
    order_id: str
