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
from shared.messaging.kafka_publisher import (
    check_kafka_health,
    close_kafka_producer,
    get_buffered_count,
    get_buffered_events,
    init_kafka_producer,
    publish,
    start_kafka_consumer,
)

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
    "check_kafka_health",
    "close_kafka_producer",
    "get_buffered_count",
    "get_buffered_events",
    "init_kafka_producer",
    "publish",
    "start_kafka_consumer",
]
