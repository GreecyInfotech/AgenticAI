from __future__ import annotations

async def process_payment(order_id: str, amount: float) -> dict:
    return {"order_id": order_id, "status": "completed", "amount": amount}
