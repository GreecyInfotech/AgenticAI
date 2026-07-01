# AI Distributor Ordering Platform — End-to-End UML

Visual architecture and behavior models for the full platform.  
PlantUML sources: [`uml/plantuml/`](uml/plantuml/) · Render with [PlantUML](https://plantuml.com/) or VS Code PlantUML extension.

---

## 1. System Context (C4 Level 1)

```mermaid
flowchart TB
    subgraph actors [Actors]
        Distributor["Distributor User"]
        SalesRep["Sales Rep"]
        Admin["Platform Admin"]
    end

    subgraph platform [AI Distributor Ordering Platform]
        System["Ordering Platform\n(Frontend + Gateway + AI Platform + Microservices)"]
    end

    subgraph external [External Systems]
        OpenAI["LLM Providers\n(OpenAI / Ollama / Azure)"]
        CRM["CRM\n(Salesforce / REST API)"]
        SMTP["Email SMTP"]
        ERP["ERP / SAP"]
    end

    Distributor --> System
    SalesRep --> System
    Admin --> System
    System --> OpenAI
    System --> CRM
    System --> SMTP
    System --> ERP
```

---

## 2. Container Diagram (C4 Level 2)

```mermaid
flowchart LR
    subgraph clients [Clients]
        FE["Frontend\nReact + Vite :5173"]
    end

    subgraph edge [Edge]
        GW["API Gateway\n:8080"]
    end

    subgraph core [Core]
        AI["AI Platform\nFastAPI + LangGraph :8000"]
    end

    subgraph services [Microservices]
        OS["order-service :8001"]
        IS["inventory-service :8002"]
        CS["customer-service :8003"]
        PS["pricing-service :8004"]
        PAY["payment-service :8005"]
        SH["shipment-service :8006"]
        PR["promotion-service :8007"]
        NS["notification-service :8008"]
        AN["analytics-service :8009"]
    end

    subgraph data [Data & Messaging]
        PG[("PostgreSQL")]
        RD[("Redis")]
        QD[("Qdrant")]
        KF{{"Kafka"}}
    end

    subgraph obs [Observability]
        PROM["Prometheus :9090"]
        GRAF["Grafana :3000"]
    end

    FE --> GW
    GW --> AI
    GW --> OS
    GW --> IS
    GW --> CS
    AI --> PG
    AI --> RD
    AI --> QD
    AI --> KF
    OS --> KF
    IS --> KF
    AI --> PROM
```

---

## 3. Clean Architecture Layers

```mermaid
flowchart TB
    subgraph presentation [Presentation]
        API["api/v1/*\nFastAPI Routes"]
        MW["Middleware\nJWT · Audit · CORS"]
    end

    subgraph application [Application]
        UC["Use Cases"]
        CMD["Commands / Queries"]
        H["Handlers"]
        DTO["DTOs"]
    end

    subgraph domain [Domain]
        ENT["Entities"]
        VO["Value Objects"]
        PROT["Repository Protocols"]
    end

    subgraph infrastructure [Infrastructure]
        REPO["Repositories"]
        DB["database.py"]
        REDIS["redis_client.py"]
        QDRANT["qdrant_client.py"]
        KAFKA["kafka/"]
        EMAIL["email/"]
        CRM["crm/"]
    end

    API --> UC
    UC --> H
    H --> CMD
    H --> DTO
    H --> REPO
    REPO --> PROT
    REPO --> DB
    REPO --> REDIS
    H --> KAFKA
    H --> EMAIL
    H --> CRM
```

---

## 4. Application Layer — Class Diagram (CQRS)

```mermaid
classDiagram
    class PlaceOrderUseCase {
        +execute(customer_id, items) OrderResponseDTO
    }
    class CancelOrderUseCase {
        +execute(order_id, customer_id) OrderResponseDTO
    }
    class GetOrderUseCase {
        +execute(order_id) OrderResponseDTO
    }
    class ConversationUseCase {
        +execute(request) ConversationResponseDTO
    }

    class PlaceOrderHandler {
        +handle(command) OrderResponseDTO
    }
    class CancelOrderHandler {
        +handle(command) OrderResponseDTO
    }
    class ConversationHandler {
        +handle(request) ConversationResponseDTO
    }

    class PlaceOrderCommand {
        +customer_id: str
        +items: list
    }
    class CancelOrderCommand {
        +order_id: str
        +customer_id: str
    }
    class GetOrderQuery {
        +order_id: str
    }

    class OrderResponseDTO {
        +order_id: str
        +status: str
        +total: float
    }

    PlaceOrderUseCase --> PlaceOrderHandler
    CancelOrderUseCase --> CancelOrderHandler
    ConversationUseCase --> ConversationHandler
    PlaceOrderHandler --> PlaceOrderCommand
    CancelOrderHandler --> CancelOrderCommand
    GetOrderUseCase --> GetOrderQuery
    PlaceOrderHandler --> OrderResponseDTO
```

---

## 5. LangGraph Orchestrator — Activity Diagram

```mermaid
flowchart TD
    START([User Message]) --> LOAD_MEM[Load Session Memory\nRedis / In-Memory]
    LOAD_MEM --> SUP[Supervisor Node\nSupervisorAgent + LLM]
    SUP --> PARSE{Parse JSON routing\nor keyword fallback}
    PARSE -->|target_agent set| RAG{RAG needed?}
    PARSE -->|no agent| END1([END])
    RAG -->|knowledge_agent| RETRIEVE[HybridRetriever\nQdrant + Keyword]
    RAG -->|other agents| DOM[Domain Node\nSpecialist Agent + LLM]
    RETRIEVE --> DOM
    DOM --> SAVE[Save to Session Memory]
    SAVE --> EMIT[Emit Kafka Event\nconversation.completed]
    EMIT --> REPLY([Return reply + agent_results])
```

---

## 6. Sequence — Conversation (End-to-End)

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant FE as Frontend
    participant GW as Gateway
    participant API as API /conversation
    participant UC as ConversationUseCase
    participant H as ConversationHandler
    participant WF as WorkflowExecutor
    participant G as LangGraph
    participant MEM as SessionMemory
    participant SUP as SupervisorAgent
    participant RAG as KnowledgeRetriever
    participant AG as Domain Agent
    participant LLM as InstrumentedLLM
    participant KF as Kafka

    User->>FE: Type message
    FE->>GW: POST /api/v1/conversation + JWT
    GW->>API: Proxy
    API->>UC: execute(ConversationRequestDTO)
    UC->>H: handle (injection guard)
    H->>WF: run_ordering_workflow()
    WF->>G: ainvoke(state)

    G->>MEM: get_messages / summarize
    G->>SUP: supervisor_node
    SUP->>LLM: ainvoke(supervisor prompt)
    LLM-->>SUP: JSON target_agent
    SUP->>KF: conversation.routed

    alt knowledge_agent
        G->>RAG: retrieve(query)
        RAG-->>G: chunks + citations
    end

    G->>AG: domain_node
    AG->>LLM: ainvoke(domain prompt)
    LLM-->>AG: reply
    G->>MEM: add_message(user + assistant)
    G->>KF: conversation.completed
    G-->>H: final state
    H-->>UC: ConversationResponseDTO
    UC-->>API: response
    API-->>FE: JSON
    FE-->>User: Display reply
```

---

## 7. Sequence — Place Order (End-to-End)

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant FE as Frontend
    participant GW as Gateway
    participant API as API /orders
    participant IDEM as Idempotency Store
    participant UC as PlaceOrderUseCase
    participant H as PlaceOrderHandler
    participant PROD as ProductRepository
    participant INV as InventoryRepository
    participant ORD as OrderRepository
    participant KF as Kafka

    User->>FE: Place order
    FE->>GW: POST /orders + JWT + Idempotency-Key
    GW->>API: Proxy to AI Platform
    API->>IDEM: check key
    alt cached completed
        IDEM-->>API: cached OrderResponseDTO
    end
    API->>UC: execute(customer_id, items)
    UC->>H: handle(PlaceOrderCommand)
    loop each item
        H->>PROD: get_by_sku(sku)
        H->>INV: reserve(sku, qty)
    end
    H->>ORD: create(customer_id, items, total)
    H->>KF: publish(order.created)
    H-->>UC: OrderResponseDTO
    UC-->>API: result
    API->>IDEM: complete(key, result)
    API-->>FE: 201 Created
    FE-->>User: Order confirmation
```

---

## 8. Sequence — Cancel Order

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant API as API /orders/{id}/cancel
    participant UC as CancelOrderUseCase
    participant H as CancelOrderHandler
    participant ORD as OrderRepository
    participant INV as InventoryRepository
    participant KF as Kafka

    User->>API: POST cancel + JWT
    API->>UC: execute(order_id, customer_id)
    UC->>H: handle(CancelOrderCommand)
    H->>ORD: get_by_id(order_id)
    H->>ORD: cancel(order_id, reason)
    loop each line item
        H->>INV: release(sku, qty)
    end
    H->>KF: publish(order.cancelled)
    H-->>API: OrderResponseDTO
    API-->>User: 200 OK
```

---

## 9. Sequence — Platform Startup (Infrastructure)

```mermaid
sequenceDiagram
    autonumber
    participant APP as FastAPI Lifespan
    participant PG as PostgreSQL Pool
    participant RD as Redis Client
    participant QD as Qdrant Client
    participant KF as Kafka Producer
    participant TOP as Topic Admin
    participant CON as Kafka Consumer
    participant RAG as RAG Bootstrap

    APP->>PG: init_db_pool() [5s timeout]
    APP->>RD: init_redis() [5s timeout]
    APP->>QD: init_qdrant() [5s timeout]
    APP->>KF: init_kafka_producer() [5s timeout]
    APP->>TOP: ensure_topics()
    APP->>CON: start_kafka_consumer()
    APP->>RAG: bootstrap_knowledge_base()
    Note over APP: app.state.ready = true
```

---

## 10. Infrastructure Component Diagram

```mermaid
flowchart TB
    subgraph infra [ai_platform/infrastructure]
        DB["database.py\nPool · Transactions · Health"]
        REDIS["redis_client.py\nCache · Locks · TTL"]
        QDRANT["qdrant_client.py\nCollections · Health"]
        KAFKA["kafka/\nTopics · Health"]
        EMAIL["email/smtp_client.py\nSMTP · Dev log mode"]
        CRM["crm/\nMock + REST clients"]
        REPOS["repositories/\nOrder · Customer · Product · Inventory"]
    end

    subgraph shared_infra [shared/messaging]
        PUB["kafka_publisher.py\nProducer · Consumer · Buffer"]
        EVT["events/schemas.py\nDomain events"]
    end

    DB --> PG[("PostgreSQL")]
    REDIS --> RD[("Redis")]
    QDRANT --> QD[("Qdrant")]
    KAFKA --> PUB
    PUB --> KFK{{"Kafka"}}
    EMAIL --> SMTP["SMTP Server"]
    CRM --> CRMEXT["External CRM API"]
    REPOS --> DB
```

---

## 11. Order State Machine

```mermaid
stateDiagram-v2
    [*] --> created : PlaceOrderHandler
    created --> confirmed : payment / credit check
    created --> cancelled : CancelOrderHandler
    confirmed --> shipped : shipment_service
    shipped --> delivered : delivery confirmed
    cancelled --> [*]
    delivered --> [*]
```

---

## 12. Deployment Diagram (Docker Compose)

```mermaid
flowchart TB
    subgraph host [Developer Machine / Cloud VM]
        subgraph compose [docker-compose]
            FE_C["frontend :5173"]
            GW_C["gateway :8080"]
            AI_C["ai-platform :8000"]
            PG_C["postgres :5432"]
            RD_C["redis :6379"]
            QD_C["qdrant :6333"]
            ZK_C["zookeeper :2181"]
            KF_C["kafka :9092"]
            PROM_C["prometheus :9090"]
            GRAF_C["grafana :3000"]
            SVC_C["9 microservices\n:8001-8009"]
        end
    end

    FE_C --> GW_C
    GW_C --> AI_C
    GW_C --> SVC_C
    AI_C --> PG_C
    AI_C --> RD_C
    AI_C --> QD_C
    AI_C --> KF_C
    SVC_C --> KF_C
    PROM_C --> AI_C
    GRAF_C --> PROM_C
```

---

## 13. Agent Ecosystem

```mermaid
mindmap
  root((Supervisor Agent))
    order_agent
    inventory_agent
    pricing_agent
    promotion_agent
    credit_agent
    shipment_agent
    payment_agent
    recommendation_agent
    customer_agent
    knowledge_agent
    notification_agent
    analytics_agent
    document_agent
```

---

## File Index

| File | UML Type | Description |
|------|----------|-------------|
| [`uml/plantuml/01-system-context.puml`](uml/plantuml/01-system-context.puml) | C4 Context | Actors and external systems |
| [`uml/plantuml/02-container.puml`](uml/plantuml/02-container.puml) | C4 Container | Services and data stores |
| [`uml/plantuml/03-component-ai-platform.puml`](uml/plantuml/03-component-ai-platform.puml) | Component | AI platform internal modules |
| [`uml/plantuml/04-class-application.puml`](uml/plantuml/04-class-application.puml) | Class | CQRS application layer |
| [`uml/plantuml/05-class-infrastructure.puml`](uml/plantuml/05-class-infrastructure.puml) | Class | Infrastructure clients |
| [`uml/plantuml/06-sequence-conversation.puml`](uml/plantuml/06-sequence-conversation.puml) | Sequence | AI conversation E2E |
| [`uml/plantuml/07-sequence-place-order.puml`](uml/plantuml/07-sequence-place-order.puml) | Sequence | Order placement E2E |
| [`uml/plantuml/08-sequence-cancel-order.puml`](uml/plantuml/08-sequence-cancel-order.puml) | Sequence | Order cancellation |
| [`uml/plantuml/09-sequence-startup.puml`](uml/plantuml/09-sequence-startup.puml) | Sequence | Lifespan / infra init |
| [`uml/plantuml/10-activity-orchestrator.puml`](uml/plantuml/10-activity-orchestrator.puml) | Activity | LangGraph routing flow |
| [`uml/plantuml/11-state-order.puml`](uml/plantuml/11-state-order.puml) | State | Order lifecycle |
| [`uml/plantuml/12-deployment.puml`](uml/plantuml/12-deployment.puml) | Deployment | Docker Compose topology |

### Render PlantUML

```bash
# Install PlantUML, then:
plantuml uml/plantuml/*.puml -o ../output
```

Or use the VS Code **PlantUML** extension: open any `.puml` file and press `Alt+D` to preview.

---

*AI Distributor Ordering Platform · UML v1.0 · July 2026*
