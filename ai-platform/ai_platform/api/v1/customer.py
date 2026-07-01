from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from ai_platform.config.dependencies import get_customer_repository
from shared.common.pagination import PaginatedResponse, PaginationParams, decode_cursor, paginate
from shared.security import CurrentUser, require_permission

router = APIRouter()


@router.get("/customers/{customer_id}")
async def get_customer(
    customer_id: str,
    user: Annotated[CurrentUser, Depends(require_permission("customers:read"))],
) -> dict:
    if customer_id != user.subject and user.role != "admin":
        customer_id = user.subject
    repo = get_customer_repository()
    return await repo.get_by_id(customer_id)


@router.get("/customers")
async def list_customers(
    params: Annotated[PaginationParams, Depends()],
    _user: Annotated[CurrentUser, Depends(require_permission("customers:read"))],
) -> PaginatedResponse[dict]:
    repo = get_customer_repository()
    offset = decode_cursor(params.cursor)
    customers = await repo.list_customers(limit=params.limit, offset=offset)
    return paginate(customers, limit=params.limit, cursor=params.cursor)
