from __future__ import annotations

from pydantic import BaseModel


class PromotionEntity(BaseModel):
    id: str
    name: str
