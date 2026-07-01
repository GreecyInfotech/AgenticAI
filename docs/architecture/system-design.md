# System Design

Detailed component design for the AI Distributor Ordering Platform.

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.13+ |
| API Framework | FastAPI | 0.115+ |
| AI Orchestration | LangGraph | 0.2+ |
| LLM | OpenAI / Ollama / Azure OpenAI | — |
| Vector DB | Qdrant | 1.12 |
| Message Bus | Kafka (Confluent) | 7.6 |
| Relational DB | PostgreSQL | 16 |
| Cache | Redis | 7 |
| Frontend | React + Vite + TypeScript | 19 / 6 |
| Observability | Prometheus + Grafana | — |
| Logging | structlog | 24+ |
| Testing | pytest + pytest-asyncio | 8+ |

## AI Platform Internal Structure

```
ai-platform/ai_platform/
├── api/v1/              # FastAPI route handlers
│   ├── auth.py          # JWT token issuance
│   ├── conversation.py  # AI chat endpoint
│   ├── orders.py        # Order CRUD
│   ├── products.py      # Product catalog
│   ├── inventory.py     # Stock lookup
│   ├── customer.py      # Customer profiles
│   ├── health.py        # Liveness + readiness
│   └── metrics.py       # Prometheus scrape
├── app/
│   ├── factory.py       # App creation, middleware, error handlers
│   ├── lifespan.py      # Startup/shutdown (DB, Redis, Kafka)
│   └── middleware.py      # Request ID, audit logging, security headers
├── agents/              # 14 specialist agents
│   └── {name}_agent/
│       ├── agent.py       # Agent executor
│       ├── prompt.py      # Prompt builder
│       ├── schemas.py     # Input/output Pydantic models
│       ├── state.py       # LangGraph state
│       ├── tools.py       # Agent tools
│       ├── memory.py      # Session memory wrapper
│       └── tests.py       # Unit tests
├── orchestrator/
│   ├── graph.py           # LangGraph graph definition
│   ├── nodes.py           # supervisor_node, domain_node
│   ├── edges.py           # Graph edges
│   ├── router.py          # Keyword-based agent routing
│   ├── executor.py        # WorkflowExecutor
│   ├── workflow.py        # run_ordering_workflow()
│   ├── events.py          # Kafka event emission
│   └── state.py           # OrchestratorState TypedDict
├── application/
│   ├── commands/          # Command handlers (CQRS)
│   ├── use_cases/         # Application use cases
│   └── dto/               # Data transfer objects
├── domain/                # Domain entities + repository protocols
├── infrastructure/
│   ├── database.py        # asyncpg connection pool
│   ├── redis_client.py    # Redis async client
│   └── repositories/      # Postgres + in-memory implementations
├── llm/                   # LLM provider factory + guardrails
├── rag/                   # Embeddings, retriever, vector store
├── memory/                # Session, Redis, Postgres memory
├── prompts/               # Jinja2 templates, few-shots
├── security/              # JWT, prompt injection, PII, RBAC
├── tools/                 # ERP, CRM, payment external tools
└── config/
    ├── settings.py        # Pydantic settings from .env
    └── dependencies.py    # FastAPI Depends() factories
```

## Shared Library Structure

```
shared/
├── config/settings.py     # BaseServiceSettings (env vars)
├── exceptions/platform.py # PlatformError hierarchy
├── logging/configure.py   # structlog + PII masking
├── security/
│   ├── jwt.py             # Token create/decode, RBAC
│   ├── deps.py            # FastAPI auth dependencies
│   ├── pii.py             # PII mask patterns
│   └── prompt_injection.py
├── common/
│   ├── pagination.py      # cursor/limit pagination
│   ├── problem_details.py # RFC 7807 error responses
│   └── idempotency.py     # Idempotency store
├── messaging/
│   ├── kafka_publisher.py # aiokafka producer
│   └── events/schemas.py  # Pydantic domain event models
├── constants/topics.py      # Kafka topic names
├── telemetry/             # OpenTelemetry instrumentation
├── service/factory.py     # create_service_app() for microservices
└── utils/ids.py           # ID generation
```

## Microservice Design

Each service under `services/` follows the same pattern:

```
services/{name}-service/
├── app/main.py            # FastAPI app via create_service_app()
├── Dockerfile             # Uses infrastructure/docker/Dockerfile.service
└── pyproject.toml         # Service dependencies
```

| Service | Port | Domain APIs |
|---------|------|-------------|
| order-service | 8001 | `POST/GET /api/v1/orders` |
| inventory-service | 8002 | `GET /api/v1/inventory/{sku}`, reserve |
| customer-service | 8003 | `GET /api/v1/customers` |
| pricing-service | 8004 | `POST /api/v1/pricing/quote` |
| payment-service | 8005 | `POST /api/v1/payments` |
| shipment-service | 8006 | `POST/GET /api/v1/shipments` |
| promotion-service | 8007 | `POST /api/v1/promotions/apply` |
| notification-service | 8008 | `POST /api/v1/notifications/send` |
| analytics-service | 8009 | `GET /api/v1/analytics/summary` |

## Gateway Routing

| Path Prefix | Upstream |
|-------------|----------|
| `/api/v1/conversation` | ai-platform:8000 |
| `/api/v1/orders` | order-service:8080 |
| `/api/v1/inventory` | inventory-service:8080 |
| `/api/v1/products` | ai-platform:8000 |
| `/api/v1/customers` | customer-service:8080 |
| `/api/v1/auth` | ai-platform:8000 |

Public paths (no JWT): `/health`, `/ready`, `/metrics`, `/api/v1/health`, `/api/v1/auth/token`

## Degraded Mode

When Postgres, Redis, or Kafka are unavailable at startup:

- **Postgres** — repositories fall back to in-memory dictionaries with seed data
- **Redis** — session memory uses in-memory store
- **Kafka** — events buffered in memory (`get_buffered_events()`)

The API starts within 5 seconds regardless of infrastructure availability.

## Error Handling

All services use RFC 7807 Problem Details:

```json
{
  "type": "https://api.distributor.platform/errors/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "order 'ORD-999' not found",
  "instance": "/api/v1/orders/ORD-999"
}
```

## Related Documents

- [Architecture Overview](overview.md)
- [REST API](../api/rest-api.md)
- [Deployment](../deployment/docker.md)
