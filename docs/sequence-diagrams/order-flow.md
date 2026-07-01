# Order Flow Sequence Diagram

End-to-end flow for placing a distributor order.

## Manual Order (REST API)

```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend
    participant GW as Gateway
    participant API as AI Platform
    participant UC as PlaceOrderUseCase
    participant INV as InventoryRepository
    participant ORD as OrderRepository
    participant KF as Kafka

    User->>FE: Select SKU + quantity, click Place Order
    FE->>GW: POST /api/v1/orders<br/>Authorization: Bearer {jwt}<br/>Idempotency-Key: order-001
    GW->>GW: Validate JWT
    GW->>API: Proxy request
    API->>API: Check permission (orders:write)
    API->>UC: execute(customer_id, items)
    UC->>UC: Validate products, compute total
    UC->>ORD: create(customer_id, items, total)
    ORD-->>UC: order record
    UC->>INV: reserve(sku, qty, order_id)
    INV-->>UC: reservation confirmed
    UC->>KF: publish(order.created)
    UC-->>API: OrderResponseDTO
    API-->>GW: 201 Created
    GW-->>FE: Order JSON
    FE-->>User: Show order confirmation
```

## Via Gateway to Order Microservice

When the full Docker stack is running, orders route to `order-service`:

```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend
    participant GW as Gateway
    participant OS as order-service
    participant KF as Kafka

    User->>FE: Place order
    FE->>GW: POST /api/v1/orders
    GW->>OS: Proxy to order-service:8080
    OS->>OS: Create order in memory/DB
    OS->>KF: publish(order.created)
    OS-->>GW: 201 Created
    GW-->>FE: Order JSON
```

## AI-Assisted Order

```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend
    participant API as AI Platform
    participant ORCH as LangGraph
    participant SUP as supervisor_agent
    participant ORD as order_agent
    participant LLM as LLM Provider

    User->>FE: "I need 50 units of SKU-001"
    FE->>API: POST /api/v1/conversation
    API->>ORCH: run_ordering_workflow()
    ORCH->>SUP: supervisor_node
    SUP->>LLM: classify intent
    SUP-->>ORCH: route → order_agent
    ORCH->>ORD: domain_node
    ORD->>LLM: generate response
    ORD-->>ORCH: order guidance reply
    ORCH-->>API: ConversationResponse
    API-->>FE: {reply, target_agent: "order_agent"}
    FE-->>User: Display AI response
```

## Order Status Lifecycle

```
created → confirmed → shipped → delivered
                  ↘ cancelled
```

Status constants defined in `shared/constants/status.py`.
