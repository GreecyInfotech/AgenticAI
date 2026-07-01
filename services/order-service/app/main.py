from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header
from pydantic import BaseModel, Field

from shared.common.idempotency import idempotency_store
from shared.common.pagination import PaginatedResponse, PaginationParams, decode_cursor, paginate
from shared.constants.status import ORDER_STATUS_CREATED
from shared.messaging import OrderCreatedEvent, publish
from shared.security import CurrentUser, require_permission
from shared.service import create_service_app
from shared.utils.ids import generate_id

app = create_service_app(title="order-service", description="Order lifecycle microservice")

_orders: dict[str, dict] = {}


class OrderItem(BaseModel):
    sku: str
    quantity: int = Field(ge=1)
    unit_price: float = 0.0


class CreateOrderRequest(BaseModel):
    customer_id: str
    items: list[OrderItem]


class OrderResponse(BaseModel):
    order_id: str
    customer_id: str
    status: str
    total: float
    items: list[OrderItem]


@app.post("/api/v1/orders", response_model=OrderResponse, status_code=201, tags=["orders"])
async def create_order(
    body: CreateOrderRequest,
    user: Annotated[CurrentUser, Depends(require_permission("orders:write"))],
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> OrderResponse:
    if idempotency_key:
        cached = await idempotency_store.get(idempotency_key)
        if cached and cached.get("status") == "completed":
            return OrderResponse(**cached["response"])
        await idempotency_store.set(idempotency_key, {"status": "processing"})

    customer_id = body.customer_id if user.role == "admin" else user.subject
    total = sum(item.unit_price * item.quantity for item in body.items) or sum(item.quantity for item in body.items)
    order_id = generate_id("ORD")
    order = OrderResponse(
        order_id=order_id,
        customer_id=customer_id,
        status=ORDER_STATUS_CREATED,
        total=float(total),
        items=body.items,
    )
    _orders[order_id] = order.model_dump()
    event = OrderCreatedEvent.create(order_id, customer_id, float(total), [i.model_dump() for i in body.items])
    await publish(event.event_type, event)
    if idempotency_key:
        await idempotency_store.complete(idempotency_key, order.model_dump())
    return order


@app.get("/api/v1/orders/{order_id}", response_model=OrderResponse, tags=["orders"])
async def get_order(
    order_id: str,
    _user: Annotated[CurrentUser, Depends(require_permission("orders:read"))],
) -> OrderResponse:
    from shared.exceptions import NotFoundError

    if order_id not in _orders:
        raise NotFoundError("order", order_id)
    return OrderResponse(**_orders[order_id])


@app.get("/api/v1/orders", response_model=PaginatedResponse[OrderResponse], tags=["orders"])
async def list_orders(
    params: Annotated[PaginationParams, Depends()],
    user: Annotated[CurrentUser, Depends(require_permission("orders:read"))],
) -> PaginatedResponse[OrderResponse]:
    offset = decode_cursor(params.cursor)
    orders = list(_orders.values())
    if user.role != "admin":
        orders = [o for o in orders if o["customer_id"] == user.subject]
    page = [OrderResponse(**o) for o in orders[offset : offset + params.limit]]
    return paginate(page, limit=params.limit, cursor=params.cursor)
