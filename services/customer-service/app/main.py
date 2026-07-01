from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from shared.common.pagination import PaginatedResponse, PaginationParams, decode_cursor, paginate
from shared.security import CurrentUser, require_permission
from shared.service import create_service_app

app = create_service_app(title="customer-service", description="Customer master data microservice")

_customers: dict[str, dict] = {
    "CUST-001": {"customer_id": "CUST-001", "name": "Demo Distributor", "tier": "gold", "credit_limit": 50000.0},
}


@app.get("/api/v1/customers/{customer_id}", tags=["customers"])
async def get_customer(
    customer_id: str,
    user: Annotated[CurrentUser, Depends(require_permission("customers:read"))],
) -> dict:
    from shared.exceptions import NotFoundError

    lookup_id = customer_id if user.role == "admin" else user.subject
    if lookup_id not in _customers:
        raise NotFoundError("customer", lookup_id)
    return _customers[lookup_id]


@app.get("/api/v1/customers", response_model=PaginatedResponse[dict], tags=["customers"])
async def list_customers(
    params: Annotated[PaginationParams, Depends()],
    _user: Annotated[CurrentUser, Depends(require_permission("customers:read"))],
) -> PaginatedResponse[dict]:
    offset = decode_cursor(params.cursor)
    customers = list(_customers.values())[offset : offset + params.limit]
    return paginate(customers, limit=params.limit, cursor=params.cursor)
