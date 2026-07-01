from __future__ import annotations

async def check_credit(customer_id: str, amount: float) -> dict:
    return {"customer_id": customer_id, "approved": True, "limit": 50000, "requested": amount}
