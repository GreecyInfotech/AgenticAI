from __future__ import annotations

from typing import Any

from shared.logging import get_logger

logger = get_logger(__name__)

_memory_products: list[dict[str, Any]] = [
    {"sku": "SKU-001", "name": "Widget A", "price": 29.99, "category": "widgets"},
    {"sku": "SKU-002", "name": "Widget B", "price": 49.99, "category": "widgets"},
    {"sku": "SKU-12345", "name": "Industrial Bearing", "price": 15.50, "category": "parts"},
]


class ProductRepository:
    async def list_products(self, *, limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
        from ai_platform.infrastructure.database import get_pool

        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT sku, name, price, category FROM products ORDER BY name LIMIT $1 OFFSET $2",
                    limit,
                    offset,
                )
                return [dict(row) for row in rows]
        return _memory_products[offset : offset + limit]

    async def get_by_sku(self, sku: str) -> dict[str, Any] | None:
        products = await self.list_products(limit=1000, offset=0)
        return next((p for p in products if p["sku"] == sku), None)
