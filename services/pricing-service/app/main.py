from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from shared.security import CurrentUser, require_permission
from shared.service import create_service_app

app = create_service_app(title="pricing-service", description="Pricing and quotes microservice")

_prices: dict[str, float] = {"SKU-001": 29.99, "SKU-002": 49.99, "SKU-12345": 15.50}


class QuoteRequest(BaseModel):
    sku: str
    quantity: int = 1
    customer_id: str | None = None


@app.post("/api/v1/pricing/quote", tags=["pricing"])
async def get_quote(
    body: QuoteRequest,
    _user: Annotated[CurrentUser, Depends(require_permission("inventory:read"))],
) -> dict:
    from shared.exceptions import NotFoundError

    if body.sku not in _prices:
        raise NotFoundError("product", body.sku)
    unit_price = _prices[body.sku]
    return {"sku": body.sku, "unit_price": unit_price, "quantity": body.quantity, "total": unit_price * body.quantity}
