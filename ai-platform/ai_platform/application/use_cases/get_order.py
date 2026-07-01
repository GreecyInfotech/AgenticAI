from __future__ import annotations

from ai_platform.application.dto.order_dto import OrderResponseDTO
from ai_platform.application.handlers.order_query_handlers import GetOrderHandler, ListOrdersHandler
from ai_platform.application.queries.order_queries import GetOrderQuery, ListOrdersQuery


class GetOrderUseCase:
    def __init__(self) -> None:
        self._handler = GetOrderHandler()

    async def execute(self, order_id: str) -> OrderResponseDTO:
        return await self._handler.handle(GetOrderQuery(order_id=order_id))


class ListOrdersUseCase:
    def __init__(self) -> None:
        self._handler = ListOrdersHandler()

    async def execute(
        self,
        *,
        customer_id: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[OrderResponseDTO]:
        query = ListOrdersQuery(customer_id=customer_id, limit=limit, offset=offset)
        return await self._handler.handle(query)
