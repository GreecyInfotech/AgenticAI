# AI Distributor Ordering Platform — User Manual

Complete guide to the repository layout, environment setup, configuration, and running the platform locally or with Docker.

---

## Table of Contents

1. [Platform Overview](#1-platform-overview)
2. [Prerequisites](#2-prerequisites)
3. [Repository Structure](#3-repository-structure)
4. [Folder Reference — Purpose and Importance](#4-folder-reference--purpose-and-importance)
5. [Environment Configuration](#5-environment-configuration)
6. [Initial Setup](#6-initial-setup)
7. [Running the Environment](#7-running-the-environment)
8. [API Endpoints](#8-api-endpoints)
9. [Development Workflow](#9-development-workflow)
10. [Testing](#10-testing)
11. [Docker and Production Builds](#11-docker-and-production-builds)
12. [Monitoring and Observability](#12-monitoring-and-observability)
13. [CI/CD Pipelines](#13-cicd-pipelines)
14. [Troubleshooting](#14-troubleshooting)
15. [Frontend Application](#15-frontend-application)

---

## 1. Platform Overview

The **AI Distributor Ordering Platform** is an event-driven system for B2B distributor ordering. It combines:

- **LangGraph orchestration** — routes user requests through a supervisor agent to 14 specialist agents
- **RAG (Retrieval-Augmented Generation)** — knowledge base powered by Qdrant vector store
- **LLM layer** — OpenAI, Ollama, Azure OpenAI, and other providers
- **Microservices** — order, inventory, payment, shipment, and related domain services
- **Event bus** — Kafka for asynchronous domain events between services

### High-Level Architecture

```
Frontend / Mobile
       │
       ▼
   Gateway (API entry point)
       │
       ▼
AI Platform (FastAPI + LangGraph)
  ├── Supervisor Agent → routes to specialist agents
  ├── 14 Domain Agents (order, inventory, pricing, …)
  ├── RAG (Qdrant + embeddings)
  ├── LLM providers
  └── Tools → ERP / CRM / SAP adapters
       │
       ▼ (Kafka events)
Microservices ←→ Postgres / Redis / Qdrant
```

> **Python package note:** The installable package is named `ai_platform` (underscore). It lives physically at `ai-platform/ai_platform/`. All Python imports use `from ai_platform...`.

---

## 2. Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.13+ | AI platform, shared libs, tests |
| **pip** | Latest | Dependency management |
| **Docker** | 24+ | Infrastructure containers |
| **Docker Compose** | v2+ | Multi-service local stack |
| **Git** | Any recent | Source control |
| **Make** | Optional | Shortcut commands (Linux/macOS/WSL) |
| **OpenAI API key** | — | Required when `LLM_PROVIDER=openai` |

### Optional

- **Ollama** — local LLM when `LLM_PROVIDER=ollama`
- **Azure OpenAI** — enterprise LLM when `LLM_PROVIDER=azure`
- **Node.js** — required when developing `frontend/` or `mobile/`

---

## 3. Repository Structure

```
ai-distributor-ordering-platform/
│
├── .cursor/                  # Cursor IDE rules and settings
│   ├── rules/                # AI coding standards (9 rule files)
│   └── settings.json         # Editor and Python tooling config
│
├── docs/                     # Project documentation
│   ├── architecture/         # System design docs
│   ├── sequence-diagrams/    # Interaction flow diagrams
│   ├── deployment/           # Deployment guides
│   ├── api/                  # API reference docs
│   ├── prompts/              # Prompt design documentation
│   ├── runbooks/             # Operational runbooks
│   ├── ADR/                  # Architecture Decision Records
│   └── usermanual.md         # This file
│
├── infrastructure/           # DevOps and platform infrastructure
│   ├── docker/               # Dockerfiles
│   ├── kubernetes/           # K8s manifests
│   ├── terraform/            # Cloud infrastructure as code
│   ├── helm/                 # Helm charts
│   ├── kafka/                # Kafka topic definitions
│   ├── redis/                # Redis configuration
│   ├── postgres/             # Database init scripts
│   ├── qdrant/               # Vector DB configuration
│   ├── monitoring/           # Prometheus, Grafana configs
│   └── nginx/                # Reverse proxy / load balancer
│
├── shared/                   # Cross-service Python libraries
│   ├── common/               # Shared base types and helpers
│   ├── exceptions/           # Standard exception hierarchy
│   ├── logging/              # Structured logging (structlog)
│   ├── security/             # JWT, RBAC, PII masking
│   ├── telemetry/            # OpenTelemetry instrumentation
│   ├── messaging/            # Kafka publisher + domain events
│   ├── config/               # Shared configuration loaders
│   ├── constants/            # Platform-wide constants
│   └── utils/                # Generic utility functions
│
├── gateway/                  # API Gateway (single entry point)
├── ai-platform/              # Core AI service
│   └── ai_platform/          # Python package (agents, RAG, API)
├── services/                 # Domain microservices (9 services)
├── frontend/                 # Web application (React/Next.js)
├── mobile/                   # Mobile application
├── tests/                    # Platform-wide test suites
├── scripts/                  # Code generation and utility scripts
│
├── .env                      # Local environment variables (not committed)
├── .env.example              # Environment variable template
├── docker-compose.yml        # Local infrastructure stack
├── Makefile                  # Dev command shortcuts
├── pyproject.toml            # Python project metadata and deps
└── README.md                 # Quick-start overview
```

---

## 4. Folder Reference — Purpose and Importance

### Root Files

| File | Importance |
|------|------------|
| `.env` | **Critical** — stores secrets and runtime config (DB passwords, API keys, JWT secret). Never commit to Git. |
| `.env.example` | **Required for onboarding** — template showing every variable developers must set. Copy to `.env` on first setup. |
| `docker-compose.yml` | **Critical for local dev** — spins up Postgres, Redis, Qdrant, Kafka, AI platform, Prometheus, and Grafana. |
| `pyproject.toml` | **Critical** — defines Python dependencies, build config, linting, and test settings. |
| `Makefile` | **Convenience** — shortcuts for install, lint, test, run, and Docker commands. |
| `README.md` | Quick-start reference for developers. |

---

### `.cursor/` — IDE Intelligence

| Path | Purpose | Why It Matters |
|------|---------|----------------|
| `rules/python.mdc` | Python 3.13 standards, type hints, Pydantic v2 | Ensures consistent Python code across the team |
| `rules/architecture.mdc` | Clean Architecture layer rules | Prevents business logic leaking into API or infrastructure |
| `rules/coding-standards.mdc` | Naming, function length, imports | Maintains readable, maintainable code |
| `rules/api-guidelines.mdc` | REST conventions, JWT, pagination, RFC 7807 errors | Standardizes all HTTP APIs |
| `rules/testing.mdc` | pytest, coverage targets, test organization | Enforces 80%+ coverage on application/domain layers |
| `rules/security.mdc` | Input validation, PII masking, prompt injection guards | Protects against common security vulnerabilities |
| `rules/ai-agent.mdc` | Agent module structure, tool layer, state schemas | Every agent follows the same contract |
| `rules/langgraph.mdc` | Graph definition, immutable state, event emission | Ensures correct multi-agent orchestration |
| `rules/prompt-engineering.mdc` | Prompt templates, RAG injection, token limits | Keeps LLM prompts safe and versioned |
| `settings.json` | Python interpreter path, format-on-save, Ruff formatter | Consistent editor experience in Cursor |

---

### `docs/` — Knowledge Base

| Path | Purpose | Why It Matters |
|------|---------|----------------|
| `architecture/` | System design, layer diagrams, data flows | Onboarding and architectural decisions |
| `sequence-diagrams/` | Request/response flows between components | Debugging integration issues |
| `deployment/` | Environment-specific deployment procedures | Safe releases to dev/stage/prod |
| `api/` | REST API contracts and examples | Frontend and integration team reference |
| `prompts/` | Prompt design rationale and versioning | LLM behavior auditability |
| `runbooks/` | Incident response and operational procedures | Production support playbook |
| `ADR/` | Architecture Decision Records | Historical context for design choices |

---

### `infrastructure/` — Platform Operations

| Path | Purpose | Why It Matters |
|------|---------|----------------|
| `docker/` | Dockerfiles for each service | Reproducible container builds |
| `kubernetes/` | K8s Deployment, Service, Ingress manifests | Production orchestration |
| `terraform/` | Cloud resource provisioning (VPC, AKS, RDS) | Infrastructure as code |
| `helm/` | Parameterized K8s deployments | Environment-specific releases |
| `kafka/` | Topic names and partition config | Event bus contract between services |
| `redis/` | Cache and session store config | Agent session memory, rate limiting |
| `postgres/` | Schema migrations, init scripts | Persistent relational data |
| `qdrant/` | Vector collection config | RAG knowledge base storage |
| `monitoring/` | Prometheus scrape config, Grafana dashboards | Production health visibility |
| `nginx/` | Reverse proxy, TLS termination, routing | Single public entry point |

---

### `shared/` — Cross-Cutting Libraries

Used by the AI platform and all microservices. Keeps common logic DRY and consistent.

| Path | Purpose | Why It Matters |
|------|---------|----------------|
| `common/` | Base types, mixins, shared Pydantic models | Consistent data structures platform-wide |
| `exceptions/` | `PlatformError`, `NotFoundError`, etc. | Uniform error handling and HTTP mapping |
| `logging/` | structlog configuration, PII masking in logs | Safe, structured observability |
| `security/` | JWT validation, RBAC roles/permissions | Authentication on every protected endpoint |
| `telemetry/` | OpenTelemetry traces and metrics | Distributed tracing across services |
| `messaging/` | Kafka publisher and domain event schemas | Event-driven communication contract |
| `messaging/events/` | `order_created`, `payment_completed`, etc. | Typed Kafka event payloads |
| `config/` | Shared settings loaders | Single source of truth for env vars |
| `constants/` | Topic names, status codes, magic strings | No magic strings in business logic |
| `utils/` | Date helpers, ID generators, retry utilities | Reusable non-domain helpers |

---

### `gateway/` — API Gateway

| Purpose | Why It Matters |
|---------|----------------|
| Single public entry point for all client traffic | Routes requests to AI platform or microservices; handles auth, rate limiting, and CORS at the edge |
| `main.py` | FastAPI gateway with `/health` endpoint |

In production, Nginx or a cloud API gateway sits in front of this service.

---

### `ai-platform/` — Core AI Service

The heart of the platform. Contains the LangGraph orchestrator, all 14 agents, RAG pipeline, and the main FastAPI application.

| Sub-path | Purpose | Why It Matters |
|----------|---------|----------------|
| `ai_platform/agents/` | 14 specialist agents (customer, order, inventory, …) | Each agent handles one business domain |
| `ai_platform/orchestrator/` | LangGraph graph, nodes, edges, router | Routes user intent to the correct agent |
| `ai_platform/rag/` | Embeddings, chunking, retriever, vector store | Grounds LLM responses in distributor knowledge |
| `ai_platform/llm/` | Provider factory, guardrails, cost tracker | Abstracts OpenAI/Ollama/Azure behind one interface |
| `ai_platform/memory/` | Session, Redis, Postgres memory stores | Maintains conversation context across turns |
| `ai_platform/tools/` | Inventory, pricing, ERP, CRM tool adapters | Agents call external systems through tools |
| `ai_platform/workflows/` | `place_order`, `track_shipment`, etc. | High-level business process definitions |
| `ai_platform/api/v1/` | FastAPI route handlers | HTTP interface for clients |
| `ai_platform/domain/` | Entities, repositories, domain services | Clean Architecture domain layer |
| `ai_platform/application/` | Use cases, commands, queries, DTOs | Application business logic |
| `ai_platform/infrastructure/` | DB, Kafka, Qdrant, Redis adapters | External system implementations |
| `ai_platform/prompts/` | Jinja2 templates, few-shot examples | Versioned, auditable LLM prompts |
| `ai_platform/security/` | JWT, prompt injection, PII, RBAC | Platform-specific security guards |
| `ai_platform/config/` | `settings.py` — Pydantic settings from `.env` | Centralized runtime configuration |
| `ai_platform/tests/` | Unit and integration tests for AI platform | Quality gate before deployment |

#### The 14 Agents

| Agent | Responsibility |
|-------|----------------|
| `supervisor_agent` | Routes incoming messages to the correct specialist |
| `customer_agent` | Customer profile and account management |
| `inventory_agent` | Stock levels and availability |
| `pricing_agent` | Price quotes and discount rules |
| `promotion_agent` | Promotions and campaign eligibility |
| `credit_agent` | Credit limits and payment terms |
| `order_agent` | Order placement and validation |
| `shipment_agent` | Shipment tracking and logistics |
| `payment_agent` | Payment processing and status |
| `recommendation_agent` | Product suggestions |
| `notification_agent` | Email and SMS notifications |
| `analytics_agent` | Order and sales analytics |
| `document_agent` | Invoice and document generation |
| `knowledge_agent` | FAQ and RAG knowledge lookup |

---

### `services/` — Domain Microservices

Each service is independently deployable with its own `Dockerfile` and `pyproject.toml`. They communicate via Kafka events.

| Service | Domain | Why It Matters |
|---------|--------|----------------|
| `customer-service` | Customer master data | Source of truth for distributor accounts |
| `inventory-service` | Stock levels, reservations | Real-time availability for ordering |
| `pricing-service` | Price lists, discounts | Accurate quotes before order placement |
| `promotion-service` | Campaigns, coupons | Promotional pricing rules |
| `order-service` | Order lifecycle | Core transactional domain |
| `payment-service` | Payment processing | Financial transaction handling |
| `shipment-service` | Logistics and tracking | Fulfillment visibility |
| `notification-service` | Email, SMS, push | Customer and ops alerts |
| `analytics-service` | Reporting and metrics | Business intelligence |

---

### `frontend/` and `mobile/`

| Path | Purpose | Why It Matters |
|------|---------|----------------|
| `frontend/` | Web UI for distributors and sales reps | Primary user interface for ordering |
| `mobile/` | iOS/Android app | Field sales and mobile ordering |

Both connect to the `gateway/` and consume `/api/v1/` endpoints.

---

### `tests/` — Platform Test Suites

| Path | Purpose | Coverage Target |
|------|---------|-----------------|
| `unit/` | Isolated function and class tests | Application and domain layers (80%+) |
| `integration/` | Multi-component tests with mocked externals | Service interaction flows |
| `contract/` | Kafka event schema validation | Event bus contract stability |
| `agents/` | Agent state transition tests (no real LLM calls) | Agent behavior correctness |
| `api/` | HTTP endpoint tests | API contract compliance |
| `llm/` | LLM provider and guardrail tests | LLM layer safety |
| `rag/` | Retrieval and embedding pipeline tests | RAG accuracy |
| `security/` | Auth, injection, PII tests | Security posture |
| `load/` | Performance and throughput tests | Capacity planning |
| `performance/` | Latency benchmarks | SLA validation |

---

### `scripts/` — Developer Utilities

| Script | Purpose |
|--------|---------|
| `generate_agents.py` | Scaffold all 14 agent modules with standard files |
| `generate_domains.py` | Scaffold domain layer (entities, repos, services) |

Run these when adding new agents or domain modules to maintain consistent structure.

---

## 5. Environment Configuration

Copy the template and fill in your values:

```powershell
# Windows PowerShell
copy .env.example .env
```

```bash
# Linux / macOS
cp .env.example .env
```

### Variable Reference

#### Application

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | Environment name: `development`, `staging`, `production` |
| `APP_NAME` | `ai-distributor-ordering-platform` | Service identifier in logs and metrics |
| `LOG_LEVEL` | `INFO` | Logging verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

#### API

| Variable | Default | Description |
|----------|---------|-------------|
| `API_HOST` | `0.0.0.0` | Bind address for uvicorn |
| `API_PORT` | `8000` | HTTP port for the AI platform |

#### LLM Provider

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `openai` | Active provider: `openai`, `ollama`, `azure` |
| `OPENAI_API_KEY` | — | **Required** for OpenAI. Get from platform.openai.com |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model name for chat completions |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL (local LLM) |
| `AZURE_OPENAI_ENDPOINT` | — | Azure OpenAI resource endpoint |
| `AZURE_OPENAI_API_KEY` | — | Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT` | — | Azure deployment name |

#### Database (PostgreSQL)

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_HOST` | `localhost` | Database host. Use `postgres` inside Docker Compose |
| `POSTGRES_PORT` | `5432` | Database port |
| `POSTGRES_USER` | `distributor` | Database username |
| `POSTGRES_PASSWORD` | `distributor_secret` | Database password — **change in production** |
| `POSTGRES_DB` | `distributor_platform` | Database name |

#### Cache (Redis)

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `localhost` | Redis host. Use `redis` inside Docker Compose |
| `REDIS_PORT` | `6379` | Redis port |

#### Vector Store (Qdrant)

| Variable | Default | Description |
|----------|---------|-------------|
| `QDRANT_HOST` | `localhost` | Qdrant host. Use `qdrant` inside Docker Compose |
| `QDRANT_PORT` | `6333` | Qdrant HTTP port |
| `QDRANT_COLLECTION` | `distributor_knowledge` | RAG knowledge base collection name |

#### Message Bus (Kafka)

| Variable | Default | Description |
|----------|---------|-------------|
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker address |

#### Security

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_SECRET` | `change-me-in-production` | **Must change in production** — signs JWT tokens |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_EXPIRE_MINUTES` | `60` | Token lifetime in minutes |

#### Observability

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` | OpenTelemetry collector endpoint |
| `LANGFUSE_PUBLIC_KEY` | — | Langfuse tracing public key (optional) |
| `LANGFUSE_SECRET_KEY` | — | Langfuse tracing secret key (optional) |
| `PROMETHEUS_PORT` | `9090` | Prometheus scrape port |

### Docker Compose vs Local Development

When running with `docker compose`, the AI platform container connects to services by **container name**:

| Service | Host inside Docker | Host on your machine |
|---------|-------------------|----------------------|
| Postgres | `postgres` | `localhost:5432` |
| Redis | `redis` | `localhost:6379` |
| Qdrant | `qdrant` | `localhost:6333` |
| Kafka | `kafka` | `localhost:9092` |
| AI Platform | `ai-platform` | `localhost:8000` |
| Prometheus | `prometheus` | `localhost:9090` |
| Grafana | `grafana` | `localhost:3000` |

For **local Python development** (uvicorn on your machine, infra in Docker), keep `.env` host values as `localhost`.

---

## 6. Initial Setup

### Step 1 — Clone the Repository

```powershell
git clone <repository-url>
cd ai-distributor-ordering-platform
```

### Step 2 — Create Python Virtual Environment

```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3.13 -m venv .venv
source .venv/bin/activate
```

> Python 3.13 is required. Verify with `python --version`.

### Step 3 — Install Dependencies

```powershell
pip install -e ".[dev]"
```

Or using Make:

```bash
make install
```

### Step 4 — Configure Environment

```powershell
copy .env.example .env
```

Edit `.env` and set at minimum:

```env
OPENAI_API_KEY=sk-your-key-here
JWT_SECRET=a-long-random-secret-string
```

### Step 5 — Start Infrastructure

```powershell
docker compose up -d
```

This starts: Postgres, Redis, Qdrant, Zookeeper, Kafka, AI Platform, Prometheus, and Grafana.

Verify all containers are healthy:

```powershell
docker compose ps
```

### Step 6 — Verify the Platform

```powershell
# Health check
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status":"UP","service":"ai-platform"}
```

---

## 7. Running the Environment

### Option A — Full Docker Stack (Recommended for First Run)

Starts everything including the AI platform container:

```powershell
docker compose up -d          # Start all services in background
docker compose logs -f ai-platform   # Follow AI platform logs
docker compose down           # Stop all services
```

| Service | URL |
|---------|-----|
| AI Platform API | http://localhost:8000 |
| OpenAPI Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/api/v1/health |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Qdrant Dashboard | http://localhost:6333/dashboard |

### Option B — Local Python Dev Server (Hot Reload)

Run infrastructure in Docker, but the AI platform directly on your machine for fast iteration:

```powershell
# Terminal 1 — infrastructure only
docker compose up -d postgres redis qdrant zookeeper kafka prometheus grafana

# Terminal 2 — AI platform with hot reload
.\.venv\Scripts\activate
make run
# Equivalent to:
# uvicorn ai_platform.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option C — Run API Gateway Separately

```powershell
uvicorn gateway.main:app --host 0.0.0.0 --port 8080 --reload
```

Gateway health: http://localhost:8080/health

### Option D — Run Individual Microservices

Each service under `services/` has its own Dockerfile and `pyproject.toml`:

```powershell
cd services/order-service
pip install -e .
uvicorn app.main:app --port 8001 --reload
```

| Service | Default Port (suggested) |
|---------|--------------------------|
| order-service | 8001 |
| inventory-service | 8002 |
| customer-service | 8003 |
| pricing-service | 8004 |
| payment-service | 8005 |
| shipment-service | 8006 |
| promotion-service | 8007 |
| notification-service | 8008 |
| analytics-service | 8009 |

### Option E — Ollama (Local LLM, No API Key)

```powershell
# Install Ollama from https://ollama.com, then:
ollama pull llama3.2
ollama serve
```

Set in `.env`:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 8. API Endpoints

All AI platform routes are prefixed with `/api/v1/`.

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/v1/health` | No | Service health status |
| `GET` | `/api/v1/metrics` | No | Prometheus metrics |
| `POST` | `/api/v1/conversation` | JWT | Send message to AI agent orchestrator |
| `GET` | `/api/v1/orders` | JWT | List orders |
| `GET` | `/api/v1/inventory` | JWT | Check inventory |
| `GET` | `/api/v1/products` | JWT | List products |
| `GET` | `/api/v1/customer` | JWT | Customer profile |

### Example — Conversation Request

```powershell
curl -X POST http://localhost:8000/api/v1/conversation `
  -H "Content-Type: application/json" `
  -d '{
    "session_id": "sess-001",
    "customer_id": "CUST-001",
    "message": "I need 50 units of product SKU-12345"
  }'
```

Response:

```json
{
  "session_id": "sess-001",
  "reply": "...",
  "target_agent": "inventory_agent",
  "agent_results": [],
  "requires_escalation": false
}
```

### Kafka Event Topics

Defined in `infrastructure/kafka/topics.txt`:

```
order.created          order.updated
inventory.checked      inventory.reserved
promotion.applied      credit.checked
payment.completed      shipment.created
notification.sent
```

Event schemas live in `shared/messaging/events/`.

---

## 9. Development Workflow

### Make Commands

```bash
make install      # pip install -e ".[dev]"
make lint         # ruff + black check
make format       # auto-fix lint and format
make typecheck    # mypy strict mode
make test         # pytest with coverage
make run          # uvicorn dev server with reload
make docker-up    # docker compose up -d
make docker-down  # docker compose down
```

### Code Quality Standards

Enforced by `.cursor/rules/` and CI:

- **Python 3.13** with mandatory type hints
- **Pydantic v2** for all schemas
- **Ruff** for linting, **Black** for formatting
- **mypy** strict mode
- **structlog** for logging (no `print()`)
- Functions under 50 lines
- Clean Architecture: presentation → application → domain → infrastructure

### Adding a New Agent

```powershell
# Option 1 — regenerate all agents
python scripts/generate_agents.py

# Option 2 — manually create under ai-platform/ai_platform/agents/<name>_agent/
# Required files: agent.py, prompt.py, schemas.py, state.py, tools.py, memory.py, tests.py
```

### Adding a New Domain Module

```powershell
python scripts/generate_domains.py
```

---

## 10. Testing

```powershell
# Run all tests with coverage
make test

# Run specific test suite
pytest tests/unit -v
pytest tests/integration -v
pytest tests/agents -v
pytest tests/security -v
pytest ai-platform/ai_platform/agents/order_agent/tests.py -v

# Run with coverage report
pytest -v --cov=ai-platform --cov=shared --cov-report=html
```

### Test Organization

| Directory | What It Tests |
|-----------|---------------|
| `tests/unit/` | Pure logic, no I/O |
| `tests/integration/` | Multi-component flows with mocked externals |
| `tests/contract/` | Kafka event schema contracts |
| `tests/agents/` | Agent state transitions (no real LLM) |
| `tests/security/` | Auth, injection, PII masking |
| `tests/load/` | Throughput under load |
| `ai-platform/tests/` | AI platform-specific unit and integration tests |

Minimum coverage target: **80%** for application and domain layers.

---

## 11. Docker and Production Builds

### Build AI Platform Image

```powershell
docker build -f infrastructure/docker/Dockerfile.ai-platform -t ai-platform:latest .
```

### Dockerfile Structure

```
infrastructure/docker/Dockerfile.ai-platform
  ├── Python 3.13-slim base
  ├── Copies pyproject.toml, ai-platform/ai_platform/, shared/
  ├── pip install -e .
  └── CMD uvicorn ai_platform.main:app
```

### Production Checklist

- [ ] Set `APP_ENV=production`
- [ ] Change `JWT_SECRET` to a cryptographically random value (64+ chars)
- [ ] Set strong `POSTGRES_PASSWORD`
- [ ] Configure `OPENAI_API_KEY` or Azure OpenAI credentials
- [ ] Enable TLS via `infrastructure/nginx/`
- [ ] Deploy with `infrastructure/kubernetes/` or `infrastructure/helm/`
- [ ] Provision cloud resources with `infrastructure/terraform/`
- [ ] Configure alerting in `infrastructure/monitoring/`

---

## 12. Monitoring and Observability

| Tool | URL | Purpose |
|------|-----|---------|
| **Prometheus** | http://localhost:9090 | Metrics collection (scrapes `/api/v1/metrics`) |
| **Grafana** | http://localhost:3000 | Dashboards and alerting |
| **OpenTelemetry** | `localhost:4317` | Distributed traces |
| **Langfuse** | Cloud | LLM call tracing and cost tracking |

Prometheus config: `infrastructure/monitoring/prometheus.yml`

Default Grafana login: `admin` / `admin` (change on first login).

---

## 13. CI/CD Pipelines

Located in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `lint.yml` | Push, PR | Ruff + Black on ai-platform, shared, gateway, tests |
| `tests.yml` | Push, PR | Full pytest suite |
| `docker.yml` | Push to `main` | Build AI platform Docker image |
| `security.yml` | Push, PR | Security scanning |
| `deploy-dev.yml` | Push to `develop` | Deploy to development environment |
| `deploy-stage.yml` | Push to `staging` | Deploy to staging environment |
| `deploy-prod.yml` | Push to `main` | Deploy to production environment |

---

## 14. Troubleshooting

### Python version error

```
ERROR: Package requires a different Python: 3.12.x not in '>=3.13'
```

**Fix:** Install Python 3.13 and recreate the virtual environment.

```powershell
python3.13 -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
```

### `ModuleNotFoundError: No module named 'ai_platform'`

**Fix:** Ensure editable install completed and `ai-platform` is on the Python path.

```powershell
pip install -e ".[dev]"
# Or set manually:
$env:PYTHONPATH = ".;ai-platform"
```

### Docker containers not starting

```powershell
docker compose ps          # Check status
docker compose logs kafka  # Check specific service logs
docker compose down -v     # Reset volumes (destroys data)
docker compose up -d       # Restart
```

### Kafka connection refused on localhost

Kafka takes 30–60 seconds to start. Wait and retry:

```powershell
docker compose logs -f kafka
```

### OpenAI API errors

- Verify `OPENAI_API_KEY` is set in `.env`
- Confirm `LLM_PROVIDER=openai`
- Check API key has sufficient credits at platform.openai.com

### Port already in use

```powershell
# Find process on port 8000 (Windows)
netstat -ano | findstr :8000

# Kill process by PID
taskkill /PID <pid> /F
```

### Database connection refused

Ensure Postgres container is running and `.env` host is correct:

- Docker Compose full stack: `POSTGRES_HOST=postgres`
- Local Python dev: `POSTGRES_HOST=localhost`

---

## 15. Frontend Application

The React web frontend provides a complete UI for the platform.

### Quick Start

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 and sign in with `CUST-001` / `distributor`.

### Pages

| Page | Route | Features |
|------|-------|----------|
| Dashboard | `/` | API status, order/product counts, quick actions |
| AI Assistant | `/conversation` | LangGraph chat with 14 agents |
| Orders | `/orders` | Create orders, view history |
| Products | `/products` | Browse catalog |
| Inventory | `/inventory` | Stock lookup by SKU |

### Configuration

```env
# frontend/.env
VITE_PROXY_TARGET=http://localhost:8000   # API target (or 8080 for gateway)
```

See [Frontend Guide](frontend.md) for full details.

---

## Quick Reference Card

```powershell
# First-time setup
copy .env.example .env
python -m venv .venv && .\.venv\Scripts\activate
pip install -e ".[dev]"
docker compose up -d

# Daily development
.\.venv\Scripts\activate
make run                              # Start API with hot reload
cd frontend && npm run dev            # Start frontend
curl http://localhost:8000/api/v1/health

# Before committing
make lint && make typecheck && make test

# Stop everything
docker compose down
```

---

*Last updated: July 2026 — AI Distributor Ordering Platform v0.1.0*
