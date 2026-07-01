# REST API Reference

Base URL: `http://localhost:8000/api/v1` (AI Platform) or `http://localhost:8080/api/v1` (Gateway)

Interactive docs: http://localhost:8000/docs

All protected endpoints require `Authorization: Bearer <token>` header.

---

## Authentication

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/auth/token` | No | Issue JWT access token |
| `GET` | `/auth/me` | Yes | Get current user profile |

See [Authentication Guide](authentication.md) for details.

---

## Health & Metrics

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | No | Liveness probe |
| `GET` | `/ready` | No | Readiness probe with dependency status |
| `GET` | `/metrics` | No | Prometheus metrics (text/plain) |

### Health Response

```json
{"status": "UP", "service": "ai-platform"}
```

### Ready Response

```json
{
  "status": "READY",
  "service": "ai-platform",
  "dependencies": {
    "postgres": {"status": "UP"},
    "redis": {"status": "DOWN", "detail": "client not initialized"}
  }
}
```

---

## Conversation (AI)

| Method | Path | Auth | Permission |
|--------|------|------|------------|
| `POST` | `/conversation` | Yes | `conversation:write` |

### Request

```json
{
  "session_id": "sess-001",
  "customer_id": "CUST-001",
  "message": "I need 50 units of SKU-001"
}
```

### Response

```json
{
  "session_id": "sess-001",
  "reply": "[mock-response] Processed request (...)",
  "target_agent": "inventory_agent",
  "agent_results": [
    {"agent": "supervisor_agent", "message": "...", "confidence": 0.85},
    {"agent": "inventory_agent", "message": "...", "confidence": 0.85}
  ],
  "requires_escalation": false
}
```

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | Bearer JWT |
| `Idempotency-Key` | No | Reserved for session deduplication |

---

## Orders

| Method | Path | Auth | Permission |
|--------|------|------|------------|
| `POST` | `/orders` | Yes | `orders:write` |
| `GET` | `/orders` | Yes | `orders:read` |
| `GET` | `/orders/{order_id}` | Yes | `orders:read` |

### Create Order

```json
POST /api/v1/orders
Idempotency-Key: order-unique-001

{
  "customer_id": "CUST-001",
  "items": [
    {"sku": "SKU-001", "quantity": 10}
  ]
}
```

### Response (201)

```json
{
  "order_id": "ORD-A1B2C3D4E5F6",
  "customer_id": "CUST-001",
  "status": "created",
  "total": 299.90,
  "items": [
    {"sku": "SKU-001", "quantity": 10, "unit_price": 29.99, "line_total": 299.90}
  ]
}
```

### List Orders (paginated)

```
GET /api/v1/orders?limit=20&cursor=0
```

```json
{
  "items": [...],
  "next_cursor": "20",
  "total": 5
}
```

---

## Products

| Method | Path | Auth | Permission |
|--------|------|------|------------|
| `GET` | `/products` | Yes | `inventory:read` |

```
GET /api/v1/products?limit=20&cursor=0
```

```json
{
  "items": [
    {"sku": "SKU-001", "name": "Widget A", "price": 29.99, "category": "widgets"},
    {"sku": "SKU-002", "name": "Widget B", "price": 49.99, "category": "widgets"}
  ],
  "next_cursor": null,
  "total": 3
}
```

---

## Inventory

| Method | Path | Auth | Permission |
|--------|------|------|------------|
| `GET` | `/inventory/{sku}` | Yes | `inventory:read` |

```json
{"sku": "SKU-001", "available": 500, "warehouse": "WH-01"}
```

---

## Customers

| Method | Path | Auth | Permission |
|--------|------|------|------------|
| `GET` | `/customers` | Yes | `customers:read` |
| `GET` | `/customers/{customer_id}` | Yes | `customers:read` |

Non-admin users can only access their own customer record.

```json
{"customer_id": "CUST-001", "name": "Demo Distributor", "tier": "gold", "credit_limit": 50000.0}
```

---

## Microservice APIs (via Gateway)

When running the full Docker stack, these endpoints are routed to microservices:

| Service | Endpoint | Method |
|---------|----------|--------|
| order-service | `/api/v1/orders` | POST, GET |
| inventory-service | `/api/v1/inventory/{sku}` | GET |
| inventory-service | `/api/v1/inventory/{sku}/reserve` | POST |
| customer-service | `/api/v1/customers` | GET |
| pricing-service | `/api/v1/pricing/quote` | POST |
| payment-service | `/api/v1/payments` | POST |
| shipment-service | `/api/v1/shipments` | POST, GET |
| promotion-service | `/api/v1/promotions/apply` | POST |
| notification-service | `/api/v1/notifications/send` | POST |
| analytics-service | `/api/v1/analytics/summary` | GET |

---

## Error Responses

All errors follow RFC 7807 Problem Details:

```json
{
  "type": "https://api.distributor.platform/errors/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "order 'ORD-999' not found",
  "instance": "/api/v1/orders/ORD-999"
}
```

| Status | Meaning |
|--------|---------|
| 401 | Missing or invalid JWT |
| 403 | Insufficient permissions |
| 404 | Resource not found |
| 409 | Idempotency conflict |
| 422 | Validation error |
| 503 | Service unavailable |

---

## Pagination

List endpoints support cursor-based pagination:

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| `limit` | 20 | 100 | Items per page |
| `cursor` | null | — | Offset cursor from previous response |

---

## Related

- [Authentication](authentication.md)
- [Kafka Events](events.md)
- [User Manual](../usermanual.md)
