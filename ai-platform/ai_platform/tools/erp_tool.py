from __future__ import annotations

async def sync_order_to_erp(order: dict) -> dict:
    return {"erp_id": "ERP-001", "status": "synced", "order": order}
