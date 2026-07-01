from __future__ import annotations

from pydantic import BaseModel


class ProductId(BaseModel):
    value: str
