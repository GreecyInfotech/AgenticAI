from __future__ import annotations

from pydantic import BaseModel


class InventoryId(BaseModel):
    value: str
