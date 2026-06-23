# Smart Port AI Platform — User Manual

**Version:** 1.0.0  
**Last updated:** June 2026  
**Audience:** Port operators, customs officers, executives, maintenance staff, system administrators, and integration developers

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Requirements](#2-system-requirements)
3. [Getting Started](#3-getting-started)
4. [User Roles and Permissions](#4-user-roles-and-permissions)
5. [Signing In](#5-signing-in)
6. [Frontend Applications](#6-frontend-applications)
7. [Working with AI Agents](#7-working-with-ai-agents)
8. [Multi-Agent Orchestration](#8-multi-agent-orchestration)
9. [Machine Learning Predictions](#9-machine-learning-predictions)
10. [Knowledge Base and RAG](#10-knowledge-base-and-rag)
11. [REST API Reference (User Guide)](#11-rest-api-reference-user-guide)
12. [Monitoring and Dashboards](#12-monitoring-and-dashboards)
13. [Enterprise Integrations (MCP)](#13-enterprise-integrations-mcp)
14. [Security and Compliance](#14-security-and-compliance)
15. [Troubleshooting](#15-troubleshooting)
16. [Frequently Asked Questions](#16-frequently-asked-questions)
17. [Glossary](#17-glossary)
18. [Appendices](#18-appendices)

---

## 1. Introduction

### 1.1 What Is the Smart Port AI Platform?

The Smart Port AI Platform is an integrated digital operations system for modern ports. It combines:

- **Real-time operational dashboards** for vessels, containers, customs, and billing
- **AI agents** that answer questions and execute tasks in natural language
- **Predictive analytics** for delays, congestion, equipment failure, and revenue
- **Knowledge retrieval (RAG)** over port manuals, SOPs, and regulatory documents
- **Enterprise integrations** via MCP (Model Context Protocol) to TOS, SAP, customs systems, and more

The platform is designed for terminal operators, planners, customs teams, executives, and IT staff who need a single interface to monitor, decide, and act across the port ecosystem.

### 1.2 Key Capabilities

| Capability | Description |
|------------|-------------|
| Vessel operations | Schedule tracking, berth allocation, ETA optimization |
| Container yard | Yard utilization, stacking, container location |
| Customs clearance | Declaration queue, risk scoring, clearance workflow |
| Billing & revenue | Invoices, tariffs, revenue summaries and forecasts |
| Maintenance | Equipment health, predictive failure, work orders |
| Safety & incidents | Hazard detection, incident triage, compliance audits |
| Logistics | Gate scheduling, truck queues, shipment tracking |
| Executive reporting | KPIs, trends, strategic briefings |

### 1.3 Platform Architecture (Overview)

```
Frontend Apps  →  API Gateway  →  Agents / ML / RAG
                      ↓
              Event Platform (Kafka)
                      ↓
              Data Platform (PostgreSQL, Redis, Elasticsearch)
```

For technical architecture details, see [architecture.md](./architecture.md).

---

## 2. System Requirements

### 2.1 End Users (Web Applications)

| Requirement | Minimum |
|-------------|---------|
| Browser | Chrome 100+, Firefox 100+, Edge 100+, Safari 16+ |
| Screen resolution | 1280 × 720 (1920 × 1080 recommended) |
| Network | Stable connection to port network or VPN |
| JavaScript | Enabled |

### 2.2 Administrators / Local Deployment

| Requirement | Version |
|-------------|---------|
| Docker & Docker Compose | Docker 24+, Compose 2.20+ |
| Node.js | 20+ |
| pnpm | 9+ |
| Python | 3.11+ |
| uv (Python package manager) | Latest |

Optional for production deployment: Kubernetes 1.28+, Helm 3.x, Terraform 1.5+, GCP/AWS/Azure account.

---

## 3. Getting Started

### 3.1 Accessing the Platform

After your administrator deploys the platform, you will receive:

- URLs for your assigned application(s)
- Username and password, **or** SSO instructions (Okta / Azure AD)
- Contact for IT support

**Default local development URLs:**

| Application | URL |
|-------------|-----|
| Port Operations UI | http://localhost:5173 |
| Executive Dashboard | http://localhost:5174 |
| Customs Dashboard | http://localhost:5175 |
| Mobile App | http://localhost:5176 |
| API Gateway (Swagger) | http://localhost:8080/api/docs |
| Agent Gateway (Swagger) | http://localhost:8081/agents/docs |
| Grafana (monitoring) | http://localhost:3000 |

### 3.2 First-Time Setup (Administrators)

If you are setting up a local or staging environment:

```bash
# 1. Copy environment configuration
cp .env.example .env

# 2. Edit .env — set JWT_SECRET, OPENAI_API_KEY (or Azure OpenAI), database passwords

# 3. Start infrastructure
make infra-up

# 4. Install dependencies
make install

# 5. Start the full stack
make dev
```

Alternatively, using Docker Compose directly:

```bash
docker compose up -d
```

Verify services are running:

```bash
curl http://localhost:8080/api/v1/health
curl http://localhost:8081/agents/v1/health
```

### 3.3 First Login Checklist

1. Open the application URL assigned to your role
2. Sign in with your credentials
3. Confirm the dashboard loads with live or sample data
4. (Optional) Test an AI agent query via the Agent Gateway or API
5. Sign out when finished on shared workstations

---

## 4. User Roles and Permissions

The platform uses **Role-Based Access Control (RBAC)**. Your administrator assigns one or more roles. Each role determines which applications, data, and actions you can access.

### 4.1 Role Summary

| Role | Primary Users | Typical Applications |
|------|---------------|----------------------|
| **admin** | IT / platform administrators | All applications and APIs |
| **operator** | Terminal operators, planners | Port Operations UI, agents, ML |
| **customs_officer** | Customs and compliance staff | Customs Dashboard, agents |
| **executive** | Port leadership, management | Executive Dashboard, billing summaries |
| **maintenance** | Equipment and facilities teams | Maintenance workflows, ML predictions |

### 4.2 Permission Matrix

| Permission | admin | operator | customs_officer | executive | maintenance |
|------------|:-----:|:--------:|:---------------:|:---------:|:-----------:|
| View vessels | ✓ | ✓ | ✓ | ✓ | — |
| Manage vessels | ✓ | ✓ | — | — | — |
| View containers | ✓ | ✓ | — | — | — |
| Manage containers | ✓ | ✓ | — | — | — |
| View customs data | ✓ | — | ✓ | — | — |
| Approve customs clearance | ✓ | — | ✓ | — | — |
| View billing | ✓ | — | — | ✓ | — |
| Manage billing | ✓ | — | — | — | — |
| Invoke AI agents | ✓ | ✓ | ✓ | ✓ | ✓ |
| Run ML predictions | ✓ | ✓ | — | — | ✓ |
| View executive KPIs | ✓ | — | — | ✓ | — |
| View/manage maintenance | ✓ | — | — | — | ✓ |
| Full admin access | ✓ | — | — | — | — |

If you attempt an action outside your permissions, the system returns **403 Forbidden**. Contact your administrator to request additional access.

### 4.3 Default Development Accounts

> **Warning:** Change all default passwords before production deployment.

| Username | Password | Role(s) |
|----------|----------|---------|
| admin | admin | admin, operator |
| operator | operator | operator |
| customs | customs | customs_officer |
| executive | executive | executive |

---

## 5. Signing In

### 5.1 Web Application Login

All four frontend applications use the same authentication flow:

1. Navigate to your application URL
2. You are redirected to the **Sign In** page if not authenticated
3. Enter your **Username** and **Password**
4. Click **Sign In**
5. On success, you are taken to the **Dashboard**

To sign out, click **Logout** in the left navigation sidebar.

### 5.2 Session Management

- Sessions are backed by a **JWT (JSON Web Token)** stored in browser local storage
- Tokens expire after **24 hours** by default
- When a token expires, you must sign in again
- Always sign out on shared or public terminals

### 5.3 Single Sign-On (SSO)

In production, your organization may use **Okta** or **Azure Active Directory (Entra ID)** instead of local passwords.

**Okta SSO:** Your administrator maps Okta groups to platform roles (e.g., `SmartPort-Operators` → operator).

**Azure AD SSO:** App roles such as `SmartPort.Admin` and `SmartPort.Operator` are mapped to platform permissions.

If SSO is enabled, click your organization's sign-in button (configured by your admin) instead of entering a local username/password.

### 5.4 API Authentication

For programmatic access (scripts, integrations, Agent Gateway):

**Step 1 — Obtain a token:**

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"operator","password":"operator"}'
```

**Step 2 — Use the token in subsequent requests:**

```bash
curl http://localhost:8080/api/v1/vessels \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 6. Frontend Applications

The platform provides four web applications, each tailored to a user persona.

### 6.1 Port Operations UI

**URL:** http://localhost:5173  
**Primary users:** Terminal operators, vessel planners, yard controllers  
**Login:** `operator` / `operator`

#### Dashboard Overview

The Port Operations dashboard displays:

| Widget | Description |
|--------|-------------|
| **Yard Utilization** | Percentage of container yard capacity in use |
| **Occupied Slots** | Number of occupied container storage positions |
| **Available Slots** | Remaining capacity in the yard |
| **Active Vessels** | Count of vessels currently in schedule |

#### Vessel Schedule Table

Below the KPI widgets, the **Vessel Schedule** table shows:

| Column | Description |
|--------|-------------|
| Vessel | Vessel name (e.g., MSC Aurora) |
| ETA | Estimated time of arrival |
| Berth | Assigned berth code (e.g., B-12) |
| Status | `approaching`, `berthed`, `scheduled`, or `departed` |

Data refreshes automatically via the API. Use this view for daily operational planning and berth coordination.

#### Typical Workflows

1. **Morning shift review** — Check yard utilization and today's vessel schedule
2. **Berth conflict** — Note overlapping ETAs and escalate to planning agent
3. **Yard capacity** — Monitor utilization; above 90% may require move planning

---

### 6.2 Executive Dashboard

**URL:** http://localhost:5174  
**Primary users:** Port directors, commercial managers, board reporting  
**Login:** `executive` / `executive`

#### Dashboard Overview

The Executive Dashboard provides high-level KPIs:

| KPI | Description |
|-----|-------------|
| vessel_calls_mtd | Vessel calls month-to-date |
| teu_handled_mtd | TEU (twenty-foot equivalent units) handled MTD |
| revenue_mtd_usd | Revenue in USD month-to-date |
| on_time_performance_pct | On-time performance percentage |

#### Revenue Trend Chart

A line chart shows revenue trend over recent months (in millions USD). Use this for board packs, investor updates, and strategic reviews.

#### Typical Workflows

1. **Weekly leadership review** — Open dashboard, export or screenshot KPIs
2. **Trend analysis** — Compare revenue and vessel call trends
3. **Agent-assisted briefing** — Use the executive agent for narrative summaries (see Section 7)

---

### 6.3 Customs Dashboard

**URL:** http://localhost:5175  
**Primary users:** Customs officers, compliance teams  
**Login:** `customs` / `customs`

#### Queue Summary

Three summary cards at the top:

| Metric | Description |
|--------|-------------|
| **Pending** | Declarations awaiting initial review |
| **In Review** | Declarations actively being processed |
| **Cleared Today** | Declarations cleared in the current day |

#### Declarations Table

| Column | Description |
|--------|-------------|
| ID | Declaration identifier (e.g., DEC-001) |
| Vessel | Associated vessel name |
| Status | `pending_review`, `cleared`, `held`, etc. |
| Risk Score | 0–100%; higher scores highlighted in red |

#### Typical Workflows

1. **Queue triage** — Sort by risk score; prioritize high-risk declarations
2. **Clearance decision** — Cross-reference with customs agent for document validation
3. **Daily reporting** — Use "Cleared Today" for shift handover

---

### 6.4 Mobile App

**URL:** http://localhost:5176  
**Primary users:** Field operators, gate staff, patrol teams  
**Login:** `operator` / `operator`

The Mobile App provides a responsive version of the Port Operations dashboard, optimized for tablets and phones. It includes:

- Yard utilization and vessel schedule (same data as Port Operations UI)
- Touch-friendly layout
- Suitable for use on the terminal floor and at gate lanes

> **Note:** For production, deploy the mobile app behind your port VPN or MDM-managed devices.

---

## 7. Working with AI Agents

The platform includes **11 domain-specific AI agents** powered by LangGraph. Each agent understands natural language queries and can call specialized tools to retrieve data or simulate actions.

### 7.1 Agent Overview

| Agent Key | Name | Port | Domain |
|-----------|------|------|--------|
| vessel | vessel-agent | 8100 | Vessel scheduling & berth allocation |
| container | container-agent | 8101 | Container yard management |
| customs | customs-agent | 8102 | Customs clearance automation |
| billing | billing-agent | 8103 | Billing & invoicing |
| maintenance | maintenance-agent | 8104 | Predictive maintenance |
| incident | incident-agent | 8105 | Incident detection & triage |
| planning | planning-agent | 8106 | Operations planning |
| safety | safety-agent | 8107 | Safety compliance |
| weather | weather-agent | 8108 | Weather impact analysis |
| logistics | logistics-agent | 8109 | Gate & drayage logistics |
| executive | executive-agent | 8110 | Executive KPI synthesis |

### 7.2 Agent Tools (Capabilities)

Each agent exposes domain-specific tools:

**Vessel Agent**
- `get_vessel_schedule` — Retrieve vessel arrival/departure schedule
- `allocate_berth` — Propose or execute berth allocation
- `predict_eta` — Estimate vessel arrival time
- `get_weather_impact` — Assess weather impact on vessel operations

**Container Agent**
- `get_container_status` — Look up container by ID or criteria
- `optimize_stacking` — Recommend yard stacking plan
- `find_container` — Locate a container in the yard
- `plan_moves` — Plan container repositioning moves

**Customs Agent**
- `check_clearance` — Check clearance status
- `submit_declaration` — Submit a customs declaration
- `validate_documents` — Validate supporting documents
- `flag_risk` — Flag high-risk shipments

**Billing Agent**
- `calculate_charges` — Compute port charges
- `generate_invoice` — Generate an invoice
- `get_tariff` — Look up tariff rates
- `reconcile_payments` — Reconcile payment records

**Maintenance Agent**
- `schedule_maintenance` — Schedule equipment maintenance
- `get_equipment_health` — Check crane/equipment health
- `predict_failure` — Predict equipment failure probability
- `create_work_order` — Create a maintenance work order

**Incident Agent**
- `detect_incident` — Detect operational incidents
- `triage_incident` — Classify and prioritize incidents
- `escalate` — Escalate to appropriate team
- `generate_report` — Generate incident report

**Planning Agent**
- `create_plan` — Create an operations plan
- `optimize_resources` — Optimize resource allocation
- `simulate_scenario` — Run what-if scenario
- `get_capacity` — Check terminal capacity

**Safety Agent**
- `check_compliance` — Verify safety compliance
- `detect_hazard` — Detect safety hazards
- `issue_alert` — Issue safety alert
- `audit_safety` — Run safety audit

**Weather Agent**
- `get_forecast` — Get weather forecast
- `assess_impact` — Assess operational impact
- `recommend_action` — Recommend operational adjustments
- `get_tide_info` — Get tide information

**Logistics Agent**
- `schedule_gate` — Schedule gate appointments
- `optimize_routes` — Optimize drayage routes
- `track_shipment` — Track shipment status
- `manage_queue` — Manage truck queue

**Executive Agent**
- `get_kpis` — Retrieve executive KPIs
- `generate_briefing` — Generate executive briefing
- `analyze_trends` — Analyze operational trends
- `compare_benchmarks` — Compare against benchmarks

### 7.3 How to Invoke an Agent

#### Via Agent Gateway (Recommended)

**Step 1:** Authenticate and save your token (see Section 5.4).

**Step 2:** List available agents:

```bash
curl http://localhost:8081/agents/v1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Step 3:** Invoke a specific agent:

```bash
curl -X POST http://localhost:8081/agents/v1/vessel/invoke \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What vessels are arriving today and which berths are available?",
    "context": {"port": "main"},
    "session_id": "my-session-001"
  }'
```

#### Response Format

```json
{
  "answer": "Based on the current schedule, three vessels are arriving today...",
  "tools_used": ["get_vessel_schedule", "allocate_berth"],
  "confidence": 0.85,
  "session_id": "my-session-001",
  "metadata": {
    "domain": "vessel",
    "agent": "vessel-agent"
  }
}
```

| Field | Description |
|-------|-------------|
| answer | Natural language response from the agent |
| tools_used | List of tools the agent invoked |
| confidence | Confidence score (0.0–1.0) |
| session_id | Session ID for follow-up queries |
| metadata | Agent and domain metadata |

### 7.4 Writing Effective Agent Queries

**Do:**
- Be specific: *"List vessels arriving between 08:00 and 18:00 tomorrow at Berth B-12"*
- Provide context in the `context` field: port code, shift, date range
- Use `session_id` for multi-turn conversations

**Avoid:**
- Vague queries: *"What's happening?"*
- Mixing unrelated domains in one query (use orchestration instead — Section 8)
- Requesting actions you are not permitted to perform (RBAC applies)

### 7.5 Example Queries by Role

**Operator**
```
"Show me yard utilization and recommend stacking changes for the MSC Aurora discharge."
"What is the truck queue length at Gate 3 right now?"
```

**Customs Officer**
```
"List all pending declarations for vessels arriving in the next 48 hours with risk score above 0.5."
"Validate documents for declaration DEC-001."
```

**Executive**
```
"Generate a weekly briefing covering vessel calls, revenue, and on-time performance."
"Compare this month's TEU volume to the same period last year."
```

**Maintenance**
```
"Which cranes have the highest predicted failure risk in the next 7 days?"
"Schedule preventive maintenance for Crane C-04 this weekend."
```

### 7.6 Agent Requirements

AI agents require an LLM provider configured in `.env`:

| Provider | Required Variables |
|----------|-------------------|
| OpenAI | `OPENAI_API_KEY` |
| Azure OpenAI | `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT` |

Without a configured LLM, agents may return errors or degraded responses. Contact your administrator.

---

## 8. Multi-Agent Orchestration

For complex questions spanning multiple domains, use the **orchestration endpoint** instead of invoking agents individually.

### 8.1 When to Use Orchestration

Use orchestration when your question involves **two or more domains**, for example:

- Vessel arrival + weather impact + berth allocation
- Container discharge + customs clearance + billing
- Incident response + safety audit + executive notification

### 8.2 How to Orchestrate

```bash
curl -X POST http://localhost:8081/agents/v1/orchestrate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "Prepare for MSC Aurora arrival tomorrow: check weather, allocate berth, and flag customs declarations"
  }'
```

### 8.3 How It Works

1. The Agent Gateway analyzes your **intent** text
2. It builds a **workflow plan** selecting relevant agents (vessel, weather, customs, etc.)
3. Each agent is invoked in sequence
4. Results are aggregated and returned in one response

### 8.4 Response Format

```json
{
  "workflow": {
    "steps": [
      { "agent": "vessel", "query": "Prepare for MSC Aurora arrival..." },
      { "agent": "weather", "query": "Prepare for MSC Aurora arrival..." },
      { "agent": "customs", "query": "Prepare for MSC Aurora arrival..." }
    ]
  },
  "results": [
    { "agent": "vessel", "result": { "answer": "...", "tools_used": [...], "confidence": 0.85 } },
    { "agent": "weather", "result": { "answer": "...", "tools_used": [...], "confidence": 0.85 } }
  ],
  "completed_at": "2026-06-23T10:30:00Z"
}
```

---

## 9. Machine Learning Predictions

The ML Platform provides seven prediction services for operational forecasting. Each service exposes a `POST /predict` endpoint.

### 9.1 Available Models

| Service | Port | Purpose |
|---------|------|---------|
| vessel-delay-prediction | 8300 | Predict vessel arrival delays (hours) |
| berth-optimization | 8301 | Optimize berth assignment |
| crane-failure-prediction | 8302 | Predict crane failure probability |
| truck-queue-prediction | 8303 | Predict gate truck queue length |
| congestion-prediction | 8304 | Predict terminal congestion level |
| anomaly-detection | 8305 | Detect anomalous operational metrics |
| revenue-forecasting | 8306 | Forecast port revenue |

### 9.2 Making a Prediction

**Example — Vessel delay prediction:**

```bash
curl -X POST http://localhost:8300/predict \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vessel_type": 1.0,
    "origin": 0.5,
    "weather_score": 0.3,
    "congestion_level": 0.7
  }'
```

**Response:**

```json
{
  "prediction": 42.5678,
  "confidence": 0.82,
  "model_version": "1.0.0",
  "features_used": ["vessel_type", "origin", "weather_score", "congestion_level"]
}
```

### 9.3 Input Features by Model

| Model | Input Features |
|-------|----------------|
| Vessel delay | vessel_type, origin, weather_score, congestion_level |
| Berth optimization | vessel_length, draft, cargo_type, priority |
| Crane failure | operating_hours, load_cycles, temperature, vibration |
| Truck queue | hour_of_day, gate_id, day_of_week, container_count |
| Congestion | vessel_count, container_moves, truck_queue, weather_score |
| Anomaly detection | metric_value, baseline, variance, time_window |
| Revenue forecast | month, vessel_calls, teu_volume, tariff_rate |

Feature values are typically normalized numerics (0.0–1.0 or raw counts). Your data science team or integration layer maps real operational data to these inputs.

### 9.4 Who Can Run Predictions

Roles with `ml:predict` permission: **admin**, **operator**, **maintenance**.

---

## 10. Knowledge Base and RAG

The RAG (Retrieval-Augmented Generation) pipeline lets agents and users search port documentation, SOPs, regulations, and manuals using semantic search.

### 10.1 RAG Pipeline Stages

| Stage | Service | Port | Function |
|-------|---------|------|----------|
| 1. Ingestion | document-ingestion | 8200 | Upload and parse documents |
| 2. Chunking | chunking | 8201 | Split documents into semantic chunks |
| 3. Embedding | embedding-service | 8202 | Generate vector embeddings |
| 4. Search | vector-search | 8203 | Similarity search over embeddings |
| 5. Metadata | metadata-extraction | 8204 | Extract entities and metadata |
| 6. Management | knowledge-management | 8205 | CRUD and lifecycle for knowledge base |

### 10.2 Searching the Knowledge Base

```bash
curl -X POST http://localhost:8203/process \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What are the berth allocation priority rules for container vessels?",
    "options": { "top_k": 5, "threshold": 0.7 }
  }'
```

**Response:**

```json
{
  "status": "success",
  "result": {
    "query": "What are the berth allocation priority rules...",
    "results": [
      {
        "document_id": "doc-001",
        "chunk_index": 0,
        "content": "Relevant port operations documentation...",
        "score": 0.92,
        "metadata": { "source": "port-manual", "section": "berth-allocation" }
      }
    ],
    "total": 2,
    "search_type": "cosine_similarity"
  }
}
```

### 10.3 Ingesting Documents (Administrators)

Typical ingestion workflow:

1. **Upload** document via document-ingestion service
2. **Chunk** content via chunking service
3. **Generate embeddings** via embedding-service
4. **Store** vectors in PostgreSQL (pgvector)
5. **Index** metadata in Elasticsearch (optional)

Agents automatically use RAG results when answering questions that reference port procedures or documentation.

### 10.4 Embedding Configuration

Configure in `.env`:

```
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=your-key
# OR
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-key
```

---

## 11. REST API Reference (User Guide)

The **API Gateway** (port 8080) is the primary REST interface. Interactive documentation is available at:

**http://localhost:8080/api/docs**

All endpoints below require `Authorization: Bearer <token>` except `/auth/login`.

### 11.1 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/login | Obtain JWT access token |

### 11.2 Vessels

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/vessels | List all vessels |
| GET | /api/v1/vessels/schedule | Get vessel schedule |

### 11.3 Containers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/containers | List containers |
| GET | /api/v1/containers/yard-status | Yard utilization metrics |

**Yard status response example:**

```json
{
  "utilization": 0.78,
  "total_slots": 5000,
  "occupied": 3900,
  "available": 1100
}
```

### 11.4 Customs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/customs/declarations | List customs declarations |
| GET | /api/v1/customs/clearance-queue | Clearance queue statistics |

### 11.5 Billing

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/billing/invoices | List invoices |
| GET | /api/v1/billing/revenue/summary | Revenue summary (MTD, YTD, growth) |

### 11.6 Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/analytics/kpis | Platform-wide KPIs |
| GET | /api/v1/analytics/dashboard/executive | Executive dashboard data |

### 11.7 Health Checks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/health | API Gateway liveness |
| GET | /api/v1/ready | Readiness (includes dependency checks) |

All backend services also expose `/health` and `/ready` on their respective ports.

For full API details, see [api-reference.md](./api-reference.md).

---

## 12. Monitoring and Dashboards

### 12.1 Grafana

**URL:** http://localhost:3000  
**Default login:** admin / admin

Grafana provides operational dashboards for:

- Vessel calls and yard utilization
- Agent invocation rates
- API Gateway latency (p95)
- Service health across the platform

The Prometheus datasource is auto-provisioned when using Docker Compose.

### 12.2 Prometheus

**URL:** http://localhost:9090

Prometheus scrapes metrics from:

- API Gateway and Agent Gateway
- All AI agents
- ML prediction services

Use Prometheus for ad-hoc queries and alert debugging.

### 12.3 Alerts

Pre-configured alert rules (see `observability/alerting/rules.yml`):

| Alert | Condition | Severity |
|-------|-----------|----------|
| ServiceDown | Service unreachable for 2 minutes | Critical |
| HighAgentLatency | p95 latency > 5 seconds for 5 minutes | Warning |
| YardUtilizationHigh | Yard utilization > 95% for 10 minutes | Warning |

Alerts are routed to your organization's notification channels (configured by administrators).

### 12.4 OpenTelemetry Tracing

Distributed traces are exported to the OTEL Collector (port 4317). Use this for debugging slow agent invocations or API requests in production observability backends (Jaeger, Datadog, etc.).

---

## 13. Enterprise Integrations (MCP)

**MCP (Model Context Protocol)** servers connect AI agents to enterprise systems. This section is primarily for administrators and integration developers.

### 13.1 Available MCP Servers

| Server | Domain | Purpose |
|--------|--------|---------|
| tos-mcp | TOS | Terminal Operating System |
| sap-mcp | SAP | ERP integration |
| postgres-mcp | PostgreSQL | Database queries |
| kafka-mcp | Kafka | Event streaming |
| customs-mcp | Customs | Customs authority systems |
| vessel-tracking-mcp | VesselTracking | AIS vessel tracking |
| billing-mcp | Billing | Billing systems |
| gate-mcp | Gate | Gate and truck management |
| crane-mcp | Crane | Crane and equipment control |
| weather-mcp | Weather | Weather data services |
| inventory-mcp | Inventory | Inventory and warehouse |
| monitoring-mcp | Monitoring | Infrastructure monitoring |

### 13.2 MCP Tools (Common Pattern)

Each MCP server exposes four standard tools:

| Tool | Description |
|------|-------------|
| `query_{domain}` | Query the system with natural language or structured query |
| `get_{domain}_status` | Get status of a resource by ID |
| `list_{domain}_resources` | List resources with optional JSON filters |
| `execute_{domain}_action` | Execute an action with JSON payload |

### 13.3 Running an MCP Server

MCP servers run via stdio for IDE and agent integration:

```bash
cd mcp-servers/tos-mcp
python src/server.py
```

Configure your AI client (Cursor, Claude Desktop, etc.) to connect to the MCP server executable path.

---

## 14. Security and Compliance

### 14.1 Authentication Methods

| Method | Use Case |
|--------|----------|
| Local JWT | Development and internal testing |
| Okta SSO | Enterprise single sign-on |
| Azure AD (Entra ID) | Microsoft-integrated organizations |

### 14.2 Authorization

All API and agent endpoints enforce RBAC. Permissions are checked on every request based on JWT role claims.

### 14.3 Audit Logging

The platform logs:

- All AI agent invocations (user, agent, query length, timestamp)
- Data access events
- Authentication events

Audit records are stored in the PostgreSQL `audit_log` table and can be indexed in Elasticsearch for search and compliance reporting.

### 14.4 Secrets Management

Production deployments should use:

- **Azure Key Vault**
- **GCP Secret Manager**
- **HashiCorp Vault**

Never commit `.env` files or API keys to source control. See `security/secrets/config.yaml` for the secrets inventory.

### 14.5 Data Protection

- All inter-service communication in production should use TLS/mTLS
- Database connections use encrypted channels (Cloud SQL, private VPC)
- Document storage supports versioning and lifecycle policies (GCS)
- Backup retention: 7 years for compliance buckets

### 14.6 User Responsibilities

- Use strong passwords; do not share credentials
- Sign out on shared devices
- Report suspicious activity to IT security
- Do not paste confidential port data into unapproved external AI tools — use the platform's built-in agents only

---

## 15. Troubleshooting

### 15.1 Cannot Sign In

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| "Invalid credentials" | Wrong username/password | Verify credentials; check Caps Lock |
| Page does not load | Service not running | Ask admin to check API Gateway: `curl localhost:8080/api/v1/health` |
| SSO redirect fails | Okta/Azure misconfiguration | Contact IT; verify `OKTA_DOMAIN` or `AZURE_AD_TENANT_ID` |
| Token expired | Session > 24 hours | Sign in again |

### 15.2 Dashboard Shows No Data

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| Empty tables | API Gateway down | Check `docker compose ps`; restart api-gateway |
| "Network Error" | CORS or proxy issue | Verify frontend proxy points to port 8080 |
| Stale data | Cache | Hard refresh (Ctrl+F5); check API directly with curl |

### 15.3 Agent Returns Error or Empty Response

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| 401 Unauthorized | Missing or expired token | Re-authenticate; include Bearer token |
| 500 Internal Server Error | LLM not configured | Set `OPENAI_API_KEY` or Azure OpenAI vars in `.env` |
| 502 Bad Gateway | Agent service down | Check agent container: `docker compose logs vessel-agent` |
| Low confidence | Ambiguous query | Rephrase with more specific context |

### 15.4 ML Prediction Fails

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| 403 Forbidden | Role lacks `ml:predict` | Request access from administrator |
| Invalid features | Wrong input format | Verify feature names and numeric types |
| Service unreachable | ML container not started | `docker compose up -d vessel-delay-prediction` |

### 15.5 Docker / Infrastructure Issues

```bash
# Check all service status
docker compose ps

# View logs for a specific service
docker compose logs -f api-gateway

# Restart a service
docker compose restart vessel-agent

# Full reset (destroys local DB data)
docker compose down -v
docker compose up -d
```

### 15.6 Getting Help

1. Check service health endpoints (`/health`, `/ready`)
2. Review Grafana dashboards for anomalies
3. Collect logs: `docker compose logs > platform-logs.txt`
4. Contact your platform administrator with: username, timestamp, URL, error message, and steps to reproduce

---

## 16. Frequently Asked Questions

**Q: Which application should I use?**  
A: Operators use **Port Operations UI**; executives use **Executive Dashboard**; customs staff use **Customs Dashboard**; field staff use the **Mobile App**.

**Q: Can I talk to the AI in plain English?**  
A: Yes. Use the Agent Gateway `/invoke` or `/orchestrate` endpoints, or integrate agents into your workflows. Write clear, specific questions.

**Q: Is my conversation with agents stored?**  
A: Agent invocations are audit-logged (user, agent, query length, timestamp). Full query text retention depends on your organization's policy — check with your administrator.

**Q: Can agents take real actions (e.g., allocate a berth)?**  
A: Agents call tools that connect to MCP servers and operational systems. Whether actions are executed or simulated depends on production integration configuration.

**Q: What LLM powers the agents?**  
A: GPT-4o via OpenAI or Azure OpenAI by default. Configured through environment variables.

**Q: How often does dashboard data refresh?**  
A: Frontend apps poll the API on load and on navigation. For real-time updates, Kafka event streaming feeds backend systems; UI refresh intervals depend on frontend configuration.

**Q: Can I access the platform from home?**  
A: Only if your organization exposes it via VPN or secure remote access. Follow your port's IT security policy.

**Q: Who do I contact for new user accounts?**  
A: Your port IT administrator or platform owner. SSO users are provisioned via Okta/Azure AD groups.

**Q: What is the difference between API Gateway and Agent Gateway?**  
A: **API Gateway** serves REST data APIs (vessels, containers, billing). **Agent Gateway** routes natural language queries to AI agents and orchestrates multi-agent workflows.

---

## 17. Glossary

| Term | Definition |
|------|------------|
| **Agent** | AI assistant specialized in one port domain (vessel, customs, etc.) |
| **AIS** | Automatic Identification System — vessel tracking |
| **Berth** | A designated mooring location for a vessel |
| **TEU** | Twenty-foot Equivalent Unit — standard container measure |
| **TOS** | Terminal Operating System |
| **MCP** | Model Context Protocol — standard for connecting AI to tools and data |
| **RAG** | Retrieval-Augmented Generation — search documents to enhance AI answers |
| **JWT** | JSON Web Token — authentication token |
| **RBAC** | Role-Based Access Control |
| **KPI** | Key Performance Indicator |
| **ETA** | Estimated Time of Arrival |
| **ETD** | Estimated Time of Departure |
| **DLQ** | Dead Letter Queue — failed Kafka messages for retry |
| **SOP** | Standard Operating Procedure |
| **SSO** | Single Sign-On |
| **pgvector** | PostgreSQL extension for vector similarity search |

---

## 18. Appendices

### Appendix A — Service Port Reference

| Service | Port |
|---------|------|
| API Gateway | 8080 |
| Agent Gateway | 8081 |
| Schema Registry | 8082 |
| Port Operations UI | 5173 |
| Executive Dashboard | 5174 |
| Customs Dashboard | 5175 |
| Mobile App | 5176 |
| Grafana | 3000 |
| Prometheus | 9090 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Elasticsearch | 9200 |
| Kafka | 9092 |
| OTEL Collector | 4317 |
| vessel-agent | 8100 |
| container-agent | 8101 |
| customs-agent | 8102 |
| billing-agent | 8103 |
| maintenance-agent | 8104 |
| incident-agent | 8105 |
| planning-agent | 8106 |
| safety-agent | 8107 |
| weather-agent | 8108 |
| logistics-agent | 8109 |
| executive-agent | 8110 |
| document-ingestion | 8200 |
| chunking | 8201 |
| embedding-service | 8202 |
| vector-search | 8203 |
| metadata-extraction | 8204 |
| knowledge-management | 8205 |
| vessel-delay-prediction | 8300 |
| berth-optimization | 8301 |
| crane-failure-prediction | 8302 |
| truck-queue-prediction | 8303 |
| congestion-prediction | 8304 |
| anomaly-detection | 8305 |
| revenue-forecasting | 8306 |

### Appendix B — Kafka Event Topics

| Topic | Domain |
|-------|--------|
| vessel.arrivals | Vessel arrivals |
| vessel.departures | Vessel departures |
| berth.allocations | Berth assignments |
| container.moves | Container movements |
| yard.status | Yard utilization updates |
| customs.declarations | Customs declarations |
| customs.clearance | Clearance events |
| billing.invoices | Invoice events |
| billing.payments | Payment events |
| incidents.created | New incidents |
| incidents.resolved | Resolved incidents |
| safety.alerts | Safety alerts |
| weather.forecasts | Weather forecasts |
| agent.invocations | Agent call audit |
| dlq.* | Dead letter queues |

### Appendix C — Related Documentation

| Document | Location | Description |
|----------|----------|-------------|
| Architecture | docs/architecture.md | System design and technology stack |
| API Reference | docs/api-reference.md | Full API endpoint reference |
| Deployment Guide | docs/deployment-guide.md | Installation and production deployment |
| README | README.md | Developer quick start |

### Appendix D — Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | June 2026 | Initial release |

---

*Smart Port AI Platform — User Manual v1.0.0*  
*For support, contact your port IT administrator.*
