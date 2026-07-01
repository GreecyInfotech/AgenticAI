from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from ai_platform.application.dto.customer_dto import CustomerResponseDTO
from ai_platform.application.use_cases.get_customer import GetCustomerUseCase, ListCustomersUseCase
from shared.common.pagination import PaginatedResponse, PaginationParams, decode_cursor, paginate
from shared.security import CurrentUser, require_permission

router = APIRouter()


@router.get("/customers/{customer_id}", response_model=CustomerResponseDTO)
async def get_customer(
    customer_id: str,
    user: Annotated[CurrentUser, Depends(require_permission("customers:read"))],
) -> CustomerResponseDTO:
    if customer_id != user.subject and user.role != "admin":
        customer_id = user.subject
    return await GetCustomerUseCase().execute(customer_id)


@router.get("/customers", response_model=PaginatedResponse[CustomerResponseDTO])
async def list_customers(
    params: Annotated[PaginationParams, Depends()],
    _user: Annotated[CurrentUser, Depends(require_permission("customers:read"))],
) -> PaginatedResponse[CustomerResponseDTO]:
    offset = decode_cursor(params.cursor)
    customers = await ListCustomersUseCase().execute(limit=params.limit, offset=offset)
    return paginate(customers, limit=params.limit, cursor=params.cursor)
