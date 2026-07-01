from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request

from ai_platform.application.dto.order_dto import CreateOrderRequestDTO, OrderResponseDTO
from ai_platform.application.use_cases.cancel_order import CancelOrderUseCase
from ai_platform.application.use_cases.get_order import GetOrderUseCase, ListOrdersUseCase
from ai_platform.application.use_cases.place_order import PlaceOrderUseCase
from shared.common.idempotency import idempotency_store
from shared.common.pagination import PaginatedResponse, PaginationParams, decode_cursor, paginate
from shared.security import CurrentUser, require_permission

router = APIRouter()


@router.post("/orders", response_model=OrderResponseDTO, status_code=201)
async def create_order(
    request: Request,
    body: CreateOrderRequestDTO,
    user: Annotated[CurrentUser, Depends(require_permission("orders:write"))],
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> OrderResponseDTO:
    if idempotency_key:
        cached = await idempotency_store.get(idempotency_key)
        if cached and cached.get("status") == "completed":
            return OrderResponseDTO(**cached["response"])
        await idempotency_store.set(idempotency_key, {"status": "processing"})

    if body.customer_id != user.subject and user.role != "admin":
        body = CreateOrderRequestDTO(customer_id=user.subject, items=body.items)

    use_case = PlaceOrderUseCase()
    result = await use_case.execute(body.customer_id, body.items)

    if idempotency_key:
        await idempotency_store.complete(idempotency_key, result.model_dump())

    return result


@router.get("/orders/{order_id}", response_model=OrderResponseDTO)
async def get_order(
    order_id: str,
    _user: Annotated[CurrentUser, Depends(require_permission("orders:read"))],
) -> OrderResponseDTO:
    return await GetOrderUseCase().execute(order_id)


@router.get("/orders", response_model=PaginatedResponse[OrderResponseDTO])
async def list_orders(
    params: Annotated[PaginationParams, Depends()],
    user: Annotated[CurrentUser, Depends(require_permission("orders:read"))],
    customer_id: str | None = None,
) -> PaginatedResponse[OrderResponseDTO]:
    offset = decode_cursor(params.cursor)
    filter_customer = customer_id if user.role == "admin" else user.subject
    orders = await ListOrdersUseCase().execute(
        customer_id=filter_customer,
        limit=params.limit,
        offset=offset,
    )
    return paginate(orders, limit=params.limit, cursor=params.cursor)


@router.post("/orders/{order_id}/cancel", response_model=OrderResponseDTO)
async def cancel_order(
    order_id: str,
    user: Annotated[CurrentUser, Depends(require_permission("orders:write"))],
    reason: str = "customer_requested",
) -> OrderResponseDTO:
    return await CancelOrderUseCase().execute(order_id, user.subject, reason=reason)
