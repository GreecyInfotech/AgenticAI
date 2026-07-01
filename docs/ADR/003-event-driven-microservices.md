# ADR-003: Event-Driven Microservices with Kafka

**Status:** Accepted  
**Date:** 2026-07-01  
**Deciders:** Platform Team

## Context

Order placement triggers multiple downstream actions: inventory reservation, payment processing, shipment creation, notifications. Synchronous coupling between services creates availability risks and makes scaling difficult.

## Decision

Adopt **event-driven architecture** with Apache Kafka:

- **10 domain topics** — one per business event type
- **Pydantic event schemas** — typed, versioned event payloads in `shared/messaging/events/`
- **Publisher abstraction** — `shared/messaging/kafka_publisher.py` with in-memory fallback
- **Contract tests** — `tests/contract/` validates event schemas
- **9 microservices** — each owns a domain, publishes and consumes events

## Event Catalog

| Event | Topic | Trigger |
|-------|-------|---------|
| Order placed | order.created | POST /orders |
| Order updated | order.updated | Status change |
| Order cancelled | order.cancelled | Cancellation |
| Stock checked | inventory.checked | GET /inventory/{sku} |
| Stock reserved | inventory.reserved | Order placement |
| Promotion applied | promotion.applied | Coupon validation |
| Credit verified | credit.checked | Credit check |
| Payment completed | payment.completed | Payment processing |
| Shipment created | shipment.created | Fulfillment |
| Notification sent | notification.sent | Email/SMS dispatch |

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|-------------|
| REST callbacks | Tight coupling, cascade failures |
| RabbitMQ | Less suited for event replay and log retention |
| Database polling | High latency, polling overhead |
| Monolith | Doesn't scale per domain |

## Consequences

### Positive

- Services scale independently
- Events can be replayed for analytics and auditing
- New consumers added without changing producers
- Contract tests prevent schema drift

### Negative

- Eventual consistency between services
- Requires Kafka infrastructure
- Debugging distributed flows is harder
- Need saga pattern for multi-step transactions

## Implementation

- Topics: `shared/constants/topics.py`, `infrastructure/kafka/topics.txt`
- Schemas: `shared/messaging/events/schemas.py`
- Publisher: `shared/messaging/kafka_publisher.py`
- Consumer: planned in `shared/messaging/kafka_consumer.py`

## References

- `.cursor/rules/architecture.mdc`
- `docs/api/events.md`
- `docs/sequence-diagrams/order-flow.md`
