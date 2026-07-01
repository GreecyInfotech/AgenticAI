from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from ai_platform.application.dto.product_dto import ProductResponseDTO
from ai_platform.application.use_cases.list_products import ListProductsUseCase
from shared.common.pagination import PaginatedResponse, PaginationParams, decode_cursor, paginate
from shared.security import CurrentUser, require_permission

router = APIRouter()


@router.get("/products", response_model=PaginatedResponse[ProductResponseDTO])
async def list_products(
    params: Annotated[PaginationParams, Depends()],
    _user: Annotated[CurrentUser, Depends(require_permission("inventory:read"))],
) -> PaginatedResponse[ProductResponseDTO]:
    offset = decode_cursor(params.cursor)
    products = await ListProductsUseCase().execute(limit=params.limit, offset=offset)
    return paginate(products, limit=params.limit, cursor=params.cursor)
