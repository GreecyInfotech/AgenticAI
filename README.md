# Enterprise Agentic AI Platform (EAAP)

Agentic enterprise platform with **B2B** and **B2C** portals, dual gateways, specialized agents, MCP servers, RAG, Kafka events, and full observability stack.

## Architecture

```
enterprise-agentic-ai-platform/
├── frontend/
│   ├── b2b-portal/          B2B dashboard (port 3001)
│   └── b2c-portal/          B2C customer assistant (port 3002)
├── api-gateway/             Unified external API (port 8000)
├── agent-gateway/           Agent orchestration (port 8001)
├── agents/
│   ├── support-agent/
│   ├── backlog-agent/
│   ├── architecture-agent/
│   ├── sales-agent/
│   └── order-agent/
├── mcp-servers/             → Python package: mcp_servers/
│   ├── github-mcp/
│   ├── jira-mcp/
│   ├── postgres-mcp/
│   ├── kafka-mcp/
│   └── filesystem-mcp/
├── rag/                     Document ingest + search (port 8002)
├── vector-store/            ChromaDB vector client
├── kafka/                   Event streaming client
├── postgres/                Operational PostgreSQL layer
├── deployment/
│   ├── cloudrun/
│   ├── terraform/
│   └── kubernetes/
└── observability/
    ├── prometheus/
    ├── grafana/
    └── opentelemetry/
```

## Request Flow

```
B2B/B2C Portal → api-gateway → agent-gateway → agents → MCP tools / RAG / Kafka / Postgres
                            ↘ rag (direct)
```

## Quick Start

```powershell
cd d:\personal\MCP\enterprise-agentic-ai-platform

python -m venv .venv
.\.venv\Scripts\activate
pip install -e .

copy .env.example .env

# Backend
.\scripts\run-local.ps1

# B2B portal (new terminal)
cd frontend\b2b-portal
npm install
npm run dev

# B2C portal (new terminal)
cd frontend\b2c-portal
npm install
npm run dev
```

| Component | URL |
|-----------|-----|
| API Gateway | http://localhost:8000 |
| Agent Gateway | http://localhost:8001 |
| RAG Service | http://localhost:8002 |
| B2B Portal | http://localhost:3001 |
| B2C Portal | http://localhost:3002 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

## Agents

| Agent | Portal | Purpose |
|-------|--------|---------|
| support-agent | B2C | Support triage, knowledge lookup |
| order-agent | B2B/B2C | Order tracking, fulfillment events |
| backlog-agent | B2B | Sprint planning, Jira backlog |
| architecture-agent | B2B | Design review, GitHub analysis |
| sales-agent | B2B | Lead qualification, pipeline |

## MCP Servers

```powershell
pip install -e .
# Entry points: mcp-github, mcp-jira, mcp-postgres, mcp-kafka, mcp-filesystem
```

Cursor config: `deployment/mcp-config.json`

## Docker Compose

```powershell
cd deployment
docker compose up --build
```

Includes Postgres, Kafka, gateways, RAG, Prometheus, and Grafana.

## License

MIT
