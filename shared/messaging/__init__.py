from __future__ import annotations

from shared.constants.topics import ALL_TOPICS
from shared.messaging.events.schemas import (
    CreditCheckedEvent,
    DomainEvent,
    InventoryCheckedEvent,
    InventoryReservedEvent,
    NotificationSentEvent,
    OrderCancelledEvent,
    OrderCreatedEvent,
    OrderUpdatedEvent,
    PaymentCompletedEvent,
    PromotionAppliedEvent,
    ShipmentCreatedEvent,
)
from shared.messaging.kafka_publisher import close_kafka_producer, get_buffered_events, init_kafka_producer, publish

__all__ = [
    "ALL_TOPICS",
    "CreditCheckedEvent",
    "DomainEvent",
    "InventoryCheckedEvent",
    "InventoryReservedEvent",
    "NotificationSentEvent",
    "OrderCancelledEvent",
    "OrderCreatedEvent",
    "OrderUpdatedEvent",
    "PaymentCompletedEvent",
    "PromotionAppliedEvent",
    "ShipmentCreatedEvent",
    "close_kafka_producer",
    "get_buffered_events",
    "init_kafka_producer",
    "publish",
]
