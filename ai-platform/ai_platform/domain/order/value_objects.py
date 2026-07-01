from __future__ import annotations

from pydantic import BaseModel


class OrderId(BaseModel):
    value: str
