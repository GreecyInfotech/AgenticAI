from __future__ import annotations

async def get_customer(customer_id: str) -> dict:
    return {"customer_id": customer_id, "name": "Demo Distributor", "tier": "gold"}
