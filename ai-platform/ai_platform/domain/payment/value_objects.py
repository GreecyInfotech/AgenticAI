from __future__ import annotations

from pydantic import BaseModel


class PaymentId(BaseModel):
    value: str
