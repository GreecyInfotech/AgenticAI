# Smart Port AI Platform

Multi-agent Smart Port Digital Transformation Platform combining operational systems, predictive ML, Agentic AI, RAG, and MCP-based enterprise integrations into a single production-grade architecture.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Frontend Applications                        │
│  Port Operations │ Executive Dashboard │ Customs │ Mobile App      │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────┐
│                     API Gateway (8080)                              │
│              REST API │ Auth │ Rate Limiting │ Swagger              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────┴────────┐   ┌────────┴────────┐   ┌────────┴────────┐
│ Agent Gateway  │   │  ML Platform    │   │  RAG Pipeline   │
│    (8081)      │   │  (7 services)   │   │  (6 services)   │
└───────┬────────┘   └─────────────────┘   └─────────────────┘
        │
┌───────┴────────────────────────────────────────────────────────┐
│                    11 AI Agents (LangGraph)                     │
│  Vessel │ Container │ Customs │ Billing │ Maintenance │ ...    │
└───────┬────────────────────────────────────────────────────────┘
        │
┌───────┴────────────────────────────────────────────────────────┐
│                    12 MCP Servers                               │
│  TOS │ SAP │ PostgreSQL │ Kafka │ Customs │ Vessel Tracking │  │
└───────┬────────────────────────────────────────────────────────┘
        │
┌───────┴────────────────────────────────────────────────────────┐
│  Data Platform          │  Event Platform  │  Observability     │
│  PostgreSQL/pgvector    │  Kafka Topics    │  Prometheus        │
│  Redis │ Elasticsearch  │  Kafka Streams   │  Grafana           │
│  BigQuery │ Cloud Storage│  Event Schemas   │  OpenTelemetry     │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ and pnpm 9+
- Python 3.11+ and uv
- (Optional) Terraform, kubectl, Helm for deployment

### Local Development

```bash
# Clone and configure
cp .env.example .env

# Start infrastructure
make infra-up

# Install dependencies
make install

# Start full stack
make dev
```

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| API Gateway | http://localhost:8080/api/docs | operator / operator |
| Agent Gateway | http://localhost:8081/agents/docs | JWT from API login |
| Port Operations UI | http://localhost:5173 | operator / operator |
| Executive Dashboard | http://localhost:5174 | executive / executive |
| Customs Dashboard | http://localhost:5175 | customs / customs |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | — |

### Authenticate

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"operator","password":"operator"}'
```

### Invoke an Agent

```bash
TOKEN="<access_token_from_login>"

curl -X POST http://localhost:8081/agents/v1/vessel/invoke \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"What vessels are arriving today and which berths are available?"}'
```

## Project Structure

```
smart-port-ai-platform/
├── frontend/               # 4 React/Vite applications
├── api-gateway/            # NestJS REST API gateway
├── agent-gateway/          # Multi-agent orchestration gateway
├── agents/                 # 11 LangGraph AI agents
├── mcp-servers/            # 12 MCP enterprise integration servers
├── rag/                    # 6 RAG pipeline services
├── ml-platform/            # 7 ML prediction services
├── event-platform/         # Kafka topics, streams, schemas, DLQ
├── data-platform/          # Database and storage configs
├── security/               # OAuth2, Okta, Azure AD, RBAC, audit
├── observability/          # Prometheus, Grafana, OpenTelemetry
├── deployment/             # Terraform, K8s, Helm, Cloud Run, CI/CD
├── shared/                 # Python and TypeScript shared libraries
└── docs/                   # Architecture and API documentation
    └── uml/                # PlantUML design artifacts (18 diagrams)
```

## Services

### AI Agents (ports 8100–8110)

| Agent | Port | Domain |
|-------|------|--------|
| vessel-agent | 8100 | Vessel scheduling & berth allocation |
| container-agent | 8101 | Container yard management |
| customs-agent | 8102 | Customs clearance automation |
| billing-agent | 8103 | Billing & invoicing |
| maintenance-agent | 8104 | Predictive maintenance |
| incident-agent | 8105 | Incident detection & triage |
| planning-agent | 8106 | Operations planning |
| safety-agent | 8107 | Safety compliance |
| weather-agent | 8108 | Weather impact analysis |
| logistics-agent | 8109 | Gate & drayage logistics |
| executive-agent | 8110 | Executive KPI synthesis |

### MCP Servers

TOS, SAP, PostgreSQL, Kafka, Customs, Vessel Tracking, Billing, Gate, Crane, Weather, Inventory, Monitoring

### ML Platform (ports 8300–8306)

Vessel delay prediction, berth optimization, crane failure prediction, truck queue prediction, congestion prediction, anomaly detection, revenue forecasting

## Deployment

### Docker Compose (local/staging)

```bash
docker compose up -d
```

### Kubernetes + Helm

```bash
make k8s-apply
make helm-install
```

### Terraform (GCP)

```bash
cp deployment/terraform/terraform.tfvars.example deployment/terraform/terraform.tfvars
make terraform-plan
make terraform-apply
```

## Development

```bash
make test          # Run all tests
make lint          # Run linters
make format        # Auto-format Python
make scaffold      # Regenerate service scaffolds
```

## License

Proprietary — Smart Port AI Platform
