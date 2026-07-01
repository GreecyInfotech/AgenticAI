from __future__ import annotations

from pydantic import BaseModel


class OrderEntity(BaseModel):
    id: str
    name: str
