from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from ai_platform.config.dependencies import get_product_repository
from shared.common.pagination import PaginatedResponse, PaginationParams, decode_cursor, paginate
from shared.security import CurrentUser, require_permission

router = APIRouter()


@router.get("/products")
async def list_products(
    params: Annotated[PaginationParams, Depends()],
    _user: Annotated[CurrentUser, Depends(require_permission("inventory:read"))],
) -> PaginatedResponse[dict]:
    repo = get_product_repository()
    offset = decode_cursor(params.cursor)
    products = await repo.list_products(limit=params.limit, offset=offset)
    return paginate(products, limit=params.limit, cursor=params.cursor)
