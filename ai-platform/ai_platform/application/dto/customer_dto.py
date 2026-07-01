from __future__ import annotations

from pydantic import BaseModel


class CustomerResponseDTO(BaseModel):
    customer_id: str
    name: str
    tier: str
    credit_limit: float = 0.0
