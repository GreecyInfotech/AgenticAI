from __future__ import annotations

import pytest

from shared.messaging.events.schemas import (
    InventoryReservedEvent,
    OrderCreatedEvent,
    PaymentCompletedEvent,
)


@pytest.mark.parametrize(
    "event_cls,factory_kwargs,expected_type",
    [
        (OrderCreatedEvent, {"order_id": "ORD-1", "customer_id": "C1", "total": 10.0, "items": []}, "order.created"),
        (InventoryReservedEvent, {"sku": "SKU-1", "quantity": 5, "order_id": "ORD-1"}, "inventory.reserved"),
        (PaymentCompletedEvent, {"order_id": "ORD-1", "amount": 99.0, "payment_id": "PAY-1"}, "payment.completed"),
    ],
)
def test_event_schemas(event_cls, factory_kwargs, expected_type) -> None:
    event = event_cls.create(**factory_kwargs)
    data = event.to_dict()
    assert data["event_type"] == expected_type
    assert "event_id" in data
    assert "timestamp" in data
    assert data["payload"]
