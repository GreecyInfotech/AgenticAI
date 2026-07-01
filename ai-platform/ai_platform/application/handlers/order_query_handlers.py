from __future__ import annotations

from ai_platform.application.dto.order_dto import OrderResponseDTO
from ai_platform.application.handlers.mappers import to_order_dto
from ai_platform.application.queries.order_queries import GetOrderQuery, ListOrdersQuery
from ai_platform.config.dependencies import get_order_repository


class GetOrderHandler:
    def __init__(self) -> None:
        self._orders = get_order_repository()

    async def handle(self, query: GetOrderQuery) -> OrderResponseDTO:
        order = await self._orders.get_by_id(query.order_id)
        return to_order_dto(order)


class ListOrdersHandler:
    def __init__(self) -> None:
        self._orders = get_order_repository()

    async def handle(self, query: ListOrdersQuery) -> list[OrderResponseDTO]:
        orders = await self._orders.list_orders(
            customer_id=query.customer_id,
            limit=query.limit,
            offset=query.offset,
        )
        return [to_order_dto(order) for order in orders]
