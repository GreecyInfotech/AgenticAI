# BFSI Agentic AI Platform

Enterprise agentic AI platform for Banking, Financial Services, and Insurance (BFSI).

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontends  │────▶│  API Gateway │────▶│     BFF     │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    ▼                          ▼                          ▼
            ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
            │ Agent Platform │          │  AI Gateway   │          │ Microservices │
            └───────┬───────┘          └───────────────┘          └───────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │ Agents │  │  RAG   │  │ Tools  │
   └────────┘  └────────┘  └────────┘
```

## Repository Structure

| Directory | Purpose |
|-----------|---------|
| `frontend/` | Customer, employee, admin portals and chatbot UI |
| `api-gateway/` | Edge routing, rate limiting, auth termination |
| `bff/` | Backend-for-frontend aggregation per persona |
| `ai-gateway/` | Model routing, prompts, tokens, caching |
| `agent-platform/` | Orchestration, workflows, memory, registry |
| `rag/` | Document ingestion, retrieval, reranking, evaluation |
| `agents/` | Domain-specific AI agents (KYC, AML, fraud, loans, etc.) |
| `tools/` | Shared tool implementations for agents |
| `messaging/` | Kafka events, schema registry, event API |
| `search/` | Elasticsearch full-text search service |
| `observability/` | Prometheus, Grafana, Loki, Tempo, OTel |
| `ci-cd/` | GitHub Actions, SonarQube, Argo CD, Nexus |
| `mcp-servers/` | MCP integrations (core banking, CRM, regulatory, etc.) |
| `microservices/` | Domain microservices |
| `databases/` | Data store configs and migrations |
| `search/` | Elasticsearch configuration |
| `messaging/` | Kafka, schema registry, connect |
| `security/` | Keycloak, Vault, PII masking, guardrails |
| `observability/` | Prometheus, Grafana, Loki, Tempo, OTel |
| `deployments/` | Docker, Kubernetes, Helm, Terraform |
| `ci-cd/` | GitHub Actions, SonarQube, Argo CD, Nexus |

## Prerequisites

- Java 21+
- Maven 3.9+
- Docker & Docker Compose
- Node.js 20+ (for frontends)

## Quick Start

```bash
# Copy environment template
cp .env.example .env

# Start infrastructure (databases, messaging, observability)
docker compose up -d

# Build all Java modules
mvn clean install -DskipTests
```

## Development

Each module under `agents/`, `microservices/`, `bff/`, and `ai-gateway/` is intended to be an independently deployable service. See module-level README files as they are added.

### Implemented layers

| Layer | Path | Port(s) |
|-------|------|---------|
| API Gateway | `api-gateway/` | 8000 |
| Customer BFF | `bff/customer-bff/` | 8101 |
| Employee BFF | `bff/employee-bff/` | 8102 |
| Admin BFF | `bff/admin-bff/` | 8103 |
| Agents | `agents/` | 8401-8414 |
| Orchestrator | `agent-platform/orchestrator/` | 8200 |
| AI Gateway | `ai-gateway/model-router/` | 8300 |
| RAG Service | `rag/rag-api/` | 8350 |
| Search API | `search/search-api/` | 8370 |
| Tools API | `tools/tools-api/` | 8450 |
| Messaging API | `messaging/messaging-api/` | 8550 |
| MCP Servers | `mcp-servers/` | 8501-8506 |
| Frontend | `frontend/` | 5173 |

```powershell
.\scripts\setup-jdk.ps1   # one-time
.\scripts\build.ps1
.\scripts\start-all.ps1    # agents + gateway + BFFs + MCP
.\scripts\start-frontend.ps1  # React UI on :5173
```

### Frontend

| Portal | Route | Description |
|--------|-------|-------------|
| Customer | `/customer` | Self-service AI banking chat |
| Employee | `/employee` | Staff chat + case escalation |
| Admin | `/admin` | Agent registry, health, debug chat |

See [frontend/README.md](frontend/README.md) for build and Docker instructions.

Example via gateway:

```bash
curl -X POST http://localhost:8000/api/customer/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"I need a home loan","customerId":"CUST-12345"}'
```

## License

Proprietary — internal use only.
