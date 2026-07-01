from __future__ import annotations

from typing import Any

from shared.exceptions import NotFoundError
from shared.logging import get_logger

logger = get_logger(__name__)

_memory_inventory: dict[str, dict[str, Any]] = {
    "SKU-001": {"sku": "SKU-001", "available": 500, "warehouse": "WH-01"},
    "SKU-12345": {"sku": "SKU-12345", "available": 120, "warehouse": "WH-01"},
}


class InventoryRepository:
    async def get_by_sku(self, sku: str) -> dict[str, Any]:
        from ai_platform.infrastructure.database import get_pool

        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT sku, available, warehouse FROM inventory WHERE sku = $1",
                    sku,
                )
                if row:
                    return dict(row)
        if sku in _memory_inventory:
            return _memory_inventory[sku]
        raise NotFoundError("inventory", sku)

    async def reserve(self, sku: str, quantity: int, order_id: str) -> dict[str, Any]:
        item = await self.get_by_sku(sku)
        if item["available"] < quantity:
            from shared.exceptions import ValidationError

            raise ValidationError(f"Insufficient stock for {sku}", details={"available": item["available"]})
        item["available"] -= quantity
        from ai_platform.infrastructure.database import get_pool

        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                await conn.execute(
                    "UPDATE inventory SET available = available - $1 WHERE sku = $2",
                    quantity,
                    sku,
                )
        logger.info("inventory_reserved", sku=sku, quantity=quantity, order_id=order_id)
        return {"sku": sku, "reserved": quantity, "order_id": order_id, "remaining": item["available"]}
