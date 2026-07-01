from __future__ import annotations

from pydantic import BaseModel


class ProductEntity(BaseModel):
    id: str
    name: str
