from __future__ import annotations

from pydantic import BaseModel


class PaymentEntity(BaseModel):
    id: str
    name: str
