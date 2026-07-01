from __future__ import annotations

from pydantic import BaseModel


class PricingId(BaseModel):
    value: str
