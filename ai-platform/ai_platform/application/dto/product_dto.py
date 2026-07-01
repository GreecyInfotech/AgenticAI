from __future__ import annotations

from pydantic import BaseModel


class ProductResponseDTO(BaseModel):
    sku: str
    name: str
    price: float
    category: str = "general"
