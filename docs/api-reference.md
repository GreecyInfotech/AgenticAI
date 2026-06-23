# API Reference

## Authentication

All authenticated endpoints require a Bearer JWT token obtained from the login endpoint.

### POST /api/v1/auth/login

```json
{
  "username": "operator",
  "password": "operator"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user": { "username": "operator", "roles": ["operator"] }
}
```

## Operational APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/vessels | List vessels |
| GET | /api/v1/vessels/schedule | Vessel schedule |
| GET | /api/v1/containers | List containers |
| GET | /api/v1/containers/yard-status | Yard utilization |
| GET | /api/v1/customs/declarations | Customs declarations |
| GET | /api/v1/customs/clearance-queue | Clearance queue stats |
| GET | /api/v1/billing/invoices | Invoices |
| GET | /api/v1/billing/revenue/summary | Revenue summary |
| GET | /api/v1/analytics/kpis | Platform KPIs |
| GET | /api/v1/analytics/dashboard/executive | Executive dashboard data |

## Agent APIs

Base URL: `http://localhost:8081/agents/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /agents | List all agents |
| POST | /{agentKey}/invoke | Invoke specific agent |
| POST | /orchestrate | Multi-agent workflow |

### Agent Invoke

```json
{
  "query": "Optimize berth allocation for tomorrow's arrivals",
  "context": { "port": "main" },
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "answer": "Based on current schedule...",
  "tools_used": ["get_vessel_schedule", "allocate_berth"],
  "confidence": 0.85,
  "session_id": "uuid",
  "metadata": { "domain": "vessel", "agent": "vessel-agent" }
}
```

## ML Prediction APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /predict | ML model inference (per service) |

### Vessel Delay Prediction

```json
{
  "vessel_type": 1.0,
  "origin": 0.5,
  "weather_score": 0.3,
  "congestion_level": 0.7
}
```

## RAG APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /process | Process document through RAG pipeline stage |

## Health Checks

All services expose:
- `GET /health` — Liveness probe
- `GET /ready` — Readiness probe with dependency checks

## Default Users

| Username | Password | Roles |
|----------|----------|-------|
| admin | admin | admin, operator |
| operator | operator | operator |
| customs | customs | customs_officer |
| executive | executive | executive |
