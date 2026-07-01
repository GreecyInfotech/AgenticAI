from __future__ import annotations

from typing import Any

async def check_inventory(sku: str, quantity: int) -> dict[str, Any]:
    return {"sku": sku, "available": 100, "requested": quantity, "reserved": False}
