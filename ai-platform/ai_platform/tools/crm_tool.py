from __future__ import annotations

async def lookup_crm(customer_id: str) -> dict:
    return {"customer_id": customer_id, "account_manager": "Jane Doe"}
