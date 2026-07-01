from __future__ import annotations

from ai_platform.application.dto.customer_dto import CustomerResponseDTO
from ai_platform.application.handlers.mappers import to_customer_dto
from ai_platform.application.queries.customer_queries import GetCustomerQuery, ListCustomersQuery
from ai_platform.config.dependencies import get_customer_repository


class GetCustomerHandler:
    def __init__(self) -> None:
        self._customers = get_customer_repository()

    async def handle(self, query: GetCustomerQuery) -> CustomerResponseDTO:
        customer = await self._customers.get_by_id(query.customer_id)
        return to_customer_dto(customer)


class ListCustomersHandler:
    def __init__(self) -> None:
        self._customers = get_customer_repository()

    async def handle(self, query: ListCustomersQuery) -> list[CustomerResponseDTO]:
        customers = await self._customers.list_customers(limit=query.limit, offset=query.offset)
        return [to_customer_dto(customer) for customer in customers]
