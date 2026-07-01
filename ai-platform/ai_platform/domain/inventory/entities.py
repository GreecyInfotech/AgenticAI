from __future__ import annotations

from pydantic import BaseModel


class InventoryEntity(BaseModel):
    id: str
    name: str
