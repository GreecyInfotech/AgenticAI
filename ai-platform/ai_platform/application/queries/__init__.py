from __future__ import annotations

from ai_platform.application.queries.catalog_queries import GetInventoryQuery, ListProductsQuery
from ai_platform.application.queries.customer_queries import GetCustomerQuery, ListCustomersQuery
from ai_platform.application.queries.order_queries import GetOrderQuery, ListOrdersQuery

__all__ = [
    "GetCustomerQuery",
    "GetInventoryQuery",
    "GetOrderQuery",
    "ListCustomersQuery",
    "ListOrdersQuery",
    "ListProductsQuery",
]
