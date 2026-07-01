from __future__ import annotations

from typing import Any

from shared.exceptions import NotFoundError
from shared.logging import get_logger

logger = get_logger(__name__)

_memory_customers: dict[str, dict[str, Any]] = {
    "CUST-001": {"customer_id": "CUST-001", "name": "Demo Distributor", "tier": "gold", "credit_limit": 50000.0},
}


class CustomerRepository:
    async def get_by_id(self, customer_id: str) -> dict[str, Any]:
        from ai_platform.infrastructure.database import get_pool

        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT customer_id, name, tier, credit_limit FROM customers WHERE customer_id = $1",
                    customer_id,
                )
                if row:
                    return dict(row)
        if customer_id in _memory_customers:
            return _memory_customers[customer_id]
        raise NotFoundError("customer", customer_id)

    async def list_customers(self, *, limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
        from ai_platform.infrastructure.database import get_pool

        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT customer_id, name, tier, credit_limit FROM customers ORDER BY name LIMIT $1 OFFSET $2",
                    limit,
                    offset,
                )
                return [dict(row) for row in rows]
        return list(_memory_customers.values())[offset : offset + limit]
