from __future__ import annotations

from ai_platform.application.dto.customer_dto import CustomerResponseDTO
from ai_platform.application.handlers.customer_query_handlers import GetCustomerHandler, ListCustomersHandler
from ai_platform.application.queries.customer_queries import GetCustomerQuery, ListCustomersQuery


class GetCustomerUseCase:
    def __init__(self) -> None:
        self._handler = GetCustomerHandler()

    async def execute(self, customer_id: str) -> CustomerResponseDTO:
        return await self._handler.handle(GetCustomerQuery(customer_id=customer_id))


class ListCustomersUseCase:
    def __init__(self) -> None:
        self._handler = ListCustomersHandler()

    async def execute(self, *, limit: int = 20, offset: int = 0) -> list[CustomerResponseDTO]:
        return await self._handler.handle(ListCustomersQuery(limit=limit, offset=offset))
