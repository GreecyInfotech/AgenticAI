from __future__ import annotations

from ai_platform.application.handlers.cancel_order_handler import CancelOrderHandler
from ai_platform.application.handlers.catalog_query_handlers import GetInventoryHandler, ListProductsHandler
from ai_platform.application.handlers.conversation_handler import ConversationHandler
from ai_platform.application.handlers.customer_query_handlers import GetCustomerHandler, ListCustomersHandler
from ai_platform.application.handlers.order_query_handlers import GetOrderHandler, ListOrdersHandler
from ai_platform.application.handlers.place_order_handler import PlaceOrderHandler
from ai_platform.application.handlers.reserve_inventory_handler import ReserveInventoryHandler

__all__ = [
    "CancelOrderHandler",
    "ConversationHandler",
    "GetCustomerHandler",
    "GetInventoryHandler",
    "GetOrderHandler",
    "ListCustomersHandler",
    "ListOrdersHandler",
    "ListProductsHandler",
    "PlaceOrderHandler",
    "ReserveInventoryHandler",
]
