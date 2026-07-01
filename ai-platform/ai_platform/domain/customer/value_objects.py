from __future__ import annotations

from pydantic import BaseModel


class CustomerId(BaseModel):
    value: str
