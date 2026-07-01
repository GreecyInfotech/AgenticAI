from __future__ import annotations

async def get_price(sku: str, customer_id: str) -> dict:
    return {"sku": sku, "unit_price": 29.99, "currency": "USD", "customer_id": customer_id}
