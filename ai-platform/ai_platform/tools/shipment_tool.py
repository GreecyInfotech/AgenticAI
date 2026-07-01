from __future__ import annotations

async def track_shipment(order_id: str) -> dict:
    return {"order_id": order_id, "status": "in_transit", "eta": "2026-07-05"}
