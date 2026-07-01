from __future__ import annotations

from pydantic import BaseModel


class CancelOrderCommand(BaseModel):
    order_id: str
    customer_id: str
    reason: str = "customer_requested"
