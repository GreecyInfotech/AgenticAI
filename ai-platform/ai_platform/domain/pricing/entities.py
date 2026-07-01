from __future__ import annotations

from pydantic import BaseModel


class PricingEntity(BaseModel):
    id: str
    name: str
