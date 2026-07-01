from __future__ import annotations

from pydantic import BaseModel


class ShipmentEntity(BaseModel):
    id: str
    name: str
