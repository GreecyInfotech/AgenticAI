# Kafka Domain Events

Event-driven communication between microservices uses Apache Kafka.

## Topics

| Topic | Producer | Consumer(s) | Description |
|-------|----------|-------------|-------------|
| `order.created` | order-service, ai-platform | analytics, notification | New order placed |
| `order.updated` | order-service | analytics, notification | Order status changed |
| `order.cancelled` | order-service | inventory, analytics | Order cancelled |
| `inventory.checked` | inventory-service, ai-platform | analytics | Stock lookup performed |
| `inventory.reserved` | inventory-service, ai-platform | order-service | Stock reserved for order |
| `promotion.applied` | promotion-service | order-service, analytics | Discount applied |
| `credit.checked` | customer-service | order-service | Credit verification |
| `payment.completed` | payment-service | order-service, notification | Payment processed |
| `shipment.created` | shipment-service | notification, analytics | Shipment dispatched |
| `notification.sent` | notification-service | analytics | Notification delivered |

Defined in `shared/constants/topics.py` and `infrastructure/kafka/topics.txt`.

## Event Schema

All events follow the `DomainEvent` base schema (Pydantic v2):

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "order.created",
  "timestamp": "2026-07-01T12:00:00.000000+00:00",
  "payload": {
    "order_id": "ORD-A1B2C3D4E5F6",
    "customer_id": "CUST-001",
    "total": 299.90,
    "items": [{"sku": "SKU-001", "quantity": 10}]
  }
}
```

## Event Classes

Located in `shared/messaging/events/schemas.py`:

| Class | event_type | Key Payload Fields |
|-------|-----------|-------------------|
| `OrderCreatedEvent` | order.created | order_id, customer_id, total, items |
| `OrderUpdatedEvent` | order.updated | order_id, status |
| `OrderCancelledEvent` | order.cancelled | order_id, reason |
| `InventoryCheckedEvent` | inventory.checked | sku, available |
| `InventoryReservedEvent` | inventory.reserved | sku, quantity, order_id |
| `PromotionAppliedEvent` | promotion.applied | order_id, promotion_code, discount |
| `CreditCheckedEvent` | credit.checked | customer_id, approved, credit_limit |
| `PaymentCompletedEvent` | payment.completed | order_id, amount, payment_id |
| `ShipmentCreatedEvent` | shipment.created | order_id, shipment_id, carrier |
| `NotificationSentEvent` | notification.sent | channel, recipient, template |

## Publishing Events

```python
from shared.messaging import OrderCreatedEvent, publish

event = OrderCreatedEvent.create(
    order_id="ORD-001",
    customer_id="CUST-001",
    total=299.90,
    items=[{"sku": "SKU-001", "quantity": 10}],
)
await publish(event.event_type, event)
```

## Kafka Configuration

```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_ENABLED=true
```

Set `KAFKA_ENABLED=false` for local development without Kafka.

When Kafka is unavailable, events are buffered in memory and logged.

## Contract Tests

Event schema validation tests are in `tests/contract/test_event_schemas.py`.

Run:

```bash
pytest tests/contract -v
```

## Internal Events

The AI platform also emits internal conversation events (not in `ALL_TOPICS`):

- `conversation.routed` — agent routing decision
- `conversation.completed` — agent response generated

These are logged and buffered but not published to Kafka topic registry.
