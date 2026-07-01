from __future__ import annotations

from pydantic import BaseModel


class CustomerEntity(BaseModel):
    id: str
    name: str
