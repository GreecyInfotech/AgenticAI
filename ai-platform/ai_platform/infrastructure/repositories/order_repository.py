from __future__ import annotations

import json
from typing import Any

from shared.constants.status import ORDER_STATUS_CANCELLED, ORDER_STATUS_CREATED
from shared.exceptions import ConflictError, NotFoundError
from shared.logging import get_logger
from shared.utils.ids import generate_id

logger = get_logger(__name__)

_memory_orders: dict[str, dict[str, Any]] = {}


class OrderRepository:
    async def create(self, customer_id: str, items: list[dict[str, Any]], total: float) -> dict[str, Any]:
        order_id = generate_id("ORD")
        order = {
            "order_id": order_id,
            "customer_id": customer_id,
            "items": items,
            "total": total,
            "status": ORDER_STATUS_CREATED,
        }
        from ai_platform.infrastructure.database import get_pool

        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO orders (order_id, customer_id, total, status, items)
                    VALUES ($1, $2, $3, $4, $5::jsonb)
                    """,
                    order_id,
                    customer_id,
                    total,
                    ORDER_STATUS_CREATED,
                    json.dumps(items),
                )
        else:
            _memory_orders[order_id] = order
        logger.info("order_created", order_id=order_id, customer_id=customer_id)
        return order

    async def get_by_id(self, order_id: str) -> dict[str, Any]:
        from ai_platform.infrastructure.database import get_pool

        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT order_id, customer_id, total, status, items FROM orders WHERE order_id = $1",
                    order_id,
                )
                if row:
                    return dict(row)
        if order_id in _memory_orders:
            return _memory_orders[order_id]
        raise NotFoundError("order", order_id)

    async def list_orders(self, *, customer_id: str | None = None, limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
        from ai_platform.infrastructure.database import get_pool

        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                if customer_id:
                    rows = await conn.fetch(
                        """
                        SELECT order_id, customer_id, total, status, items
                        FROM orders WHERE customer_id = $1
                        ORDER BY created_at DESC LIMIT $2 OFFSET $3
                        """,
                        customer_id,
                        limit,
                        offset,
                    )
                else:
                    rows = await conn.fetch(
                        """
                        SELECT order_id, customer_id, total, status, items
                        FROM orders ORDER BY created_at DESC LIMIT $1 OFFSET $2
                        """,
                        limit,
                        offset,
                    )
                return [dict(row) for row in rows]

        orders = list(_memory_orders.values())
        if customer_id:
            orders = [o for o in orders if o["customer_id"] == customer_id]
        return orders[offset : offset + limit]

    async def cancel(self, order_id: str, reason: str) -> dict[str, Any]:
        order = await self.get_by_id(order_id)
        if order["status"] == ORDER_STATUS_CANCELLED:
            raise ConflictError(f"Order {order_id} is already cancelled")

        order["status"] = ORDER_STATUS_CANCELLED
        order["cancel_reason"] = reason

        from ai_platform.infrastructure.database import get_pool

        pool = get_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                await conn.execute(
                    "UPDATE orders SET status = $1 WHERE order_id = $2",
                    ORDER_STATUS_CANCELLED,
                    order_id,
                )
        else:
            _memory_orders[order_id] = order

        logger.info("order_cancelled", order_id=order_id, reason=reason)
        return order
