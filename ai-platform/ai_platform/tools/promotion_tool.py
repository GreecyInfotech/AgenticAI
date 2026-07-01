from __future__ import annotations

async def get_promotions(customer_id: str) -> list[dict]:
    return [{"code": "SPRING10", "discount_pct": 10, "min_order": 500}]
