# AI Distributor Ordering Platform

Single-agent AI platform for distributor ordering with **LangGraph** orchestration, **14 specialist agents**, **RAG**, event-driven microservices, and a **React web frontend**.

> **Documentation:** See [docs/README.md](docs/README.md) for the complete documentation index.

## Architecture

```
Frontend/Mobile → Gateway → AI Platform (FastAPI)
                              ├── LangGraph Orchestrator
                              ├── 14 Agents (supervisor routes)
                              ├── RAG (Qdrant + embeddings)
                              ├── LLM Layer (OpenAI/Ollama/Azure)
                              └── Tools → ERP/CRM/SAP
Services (Kafka events) ←→ Postgres / Redis / Qdrant
```

> **Note:** Python package is `ai_platform` (underscore), located at `ai-platform/ai_platform/`.

## Repository Layout

```
ai-distributor-ordering-platform/
├── .cursor/rules/          # Cursor AI coding rules
├── docs/                   # Architecture, API, runbooks, ADRs
├── infrastructure/         # Docker, K8s, Terraform, Helm, monitoring
├── shared/                 # Common libs, security, messaging, config
├── gateway/                # API gateway
├── ai-platform/            # AI platform service (Python package: ai_platform)
├── services/               # Microservices (order, inventory, payment, ...)
├── frontend/
├── mobile/
├── tests/
├── scripts/
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Quick Start

```powershell
cd D:\personal\SingleAgent\ai-distributor-ordering-platform
copy .env.example .env
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"

# Infrastructure
docker compose up -d

# Run API
uvicorn ai_platform.main:app --reload --port 8000

# Run Frontend
cd frontend && npm install && npm run dev
```

| Component | URL |
|-----------|-----|
| **Frontend** | http://localhost:5173 |
| API | http://localhost:8000 |
| API Gateway | http://localhost:8080 |
| OpenAPI | http://localhost:8000/docs |
| Health | http://localhost:8000/api/v1/health |
| Conversation | POST http://localhost:8000/api/v1/conversation |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

## AI Platform Structure

```
ai-platform/ai_platform/
├── agents/           # 14 agents (customer, inventory, order, ...)
├── orchestrator/     # LangGraph graph, nodes, router
├── rag/              # Embeddings, retriever, vector store
├── llm/              # Provider factory, guardrails
├── memory/           # Session, Redis, Postgres memory
├── tools/            # Inventory, pricing, ERP, CRM tools
├── workflows/        # place_order, track_shipment, etc.
├── api/v1/           # FastAPI routes
├── domain/           # Clean architecture entities
├── application/      # Use cases, commands, queries
└── infrastructure/   # DB, Kafka, Qdrant adapters
```

## Agents

| Agent | Purpose |
|-------|---------|
| supervisor_agent | Routes to specialist agents |
| customer_agent | Customer profile |
| inventory_agent | Stock availability |
| pricing_agent | Price quotes |
| promotion_agent | Promotions |
| credit_agent | Credit checks |
| order_agent | Order placement |
| shipment_agent | Tracking |
| payment_agent | Payments |
| recommendation_agent | Product suggestions |
| notification_agent | Email/SMS |
| analytics_agent | Reporting |
| document_agent | Invoices |
| knowledge_agent | FAQ/RAG |

## Kafka Topics

- `order.created`, `order.updated`
- `inventory.checked`, `inventory.reserved`
- `promotion.applied`, `credit.checked`
- `payment.completed`, `shipment.created`, `notification.sent`

## Development

```bash
make lint      # ruff + black
make test      # pytest
make run       # uvicorn dev server
```

## Documentation

| Document | Description |
|----------|-------------|
| [docs/README.md](docs/README.md) | Documentation index |
| [User Manual](docs/usermanual.md) | Setup, configuration, troubleshooting |
| [Frontend Guide](docs/frontend.md) | React web app |
| [REST API](docs/api/rest-api.md) | API reference |
| [Architecture](docs/architecture/overview.md) | System design |
| [Deployment](docs/deployment/docker.md) | Docker Compose guide |
| [Runbooks](docs/runbooks/incident-response.md) | Operations |

## Cursor Rules

See `.cursor/rules/` for architecture, LangGraph, security, and API guidelines.

## License

Proprietary
