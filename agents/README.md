# BFSI Domain Agents

Fourteen domain-specific AI agents for the BFSI Agentic AI Platform.

## Architecture

```
User Request
     │
     ▼
┌─────────────┐     ┌──────────────────┐
│ Orchestrator│────▶│   Intent Agent   │  (classify & route)
│   :8200     │     │      :8401       │
└──────┬──────┘     └──────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│              Domain Agents (8402–8414)                    │
│  Customer │ KYC │ AML │ Fraud │ Loan │ Underwriting │ ... │
└──────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐     ┌──────────────────┐
│ Audit Agent │     │ Notification Agent│
│   :8410     │     │      :8414        │
└─────────────┘     └──────────────────┘
```

## Agents

| Agent | Port | Endpoint | Responsibility |
|-------|------|----------|----------------|
| Intent | 8401 | `/api/v1/agent/process` | Detect user intent and route requests |
| Customer | 8402 | `/api/v1/agent/process` | Customer profile, accounts, relationship 360° |
| KYC | 8403 | `/api/v1/agent/process` | Identity verification and document validation |
| AML | 8404 | `/api/v1/agent/process` | Anti-money laundering screening |
| Fraud | 8405 | `/api/v1/agent/process` | Transaction and identity fraud detection |
| Loan | 8406 | `/api/v1/agent/process` | Loan eligibility and recommendation |
| Underwriting | 8407 | `/api/v1/agent/process` | Insurance underwriting analysis |
| Claim | 8408 | `/api/v1/agent/process` | Claims validation and processing |
| Compliance | 8409 | `/api/v1/agent/process` | Regulatory checks (RBI, AML, GDPR) |
| Audit | 8410 | `/api/v1/agent/process` | Immutable audit trail and AI decision logging |
| Recommendation | 8411 | `/api/v1/agent/process` | Personalized product recommendations |
| Portfolio | 8412 | `/api/v1/agent/process` | Investment and wealth advisory |
| Escalation | 8413 | `/api/v1/agent/process` | Human handoff for complex cases |
| Notification | 8414 | `/api/v1/agent/process` | Email, SMS, push notifications |

## Build

**Prerequisites:** JDK 21 (auto-installed to `.tools/jdk-21` by setup script)

```powershell
# One-time setup (downloads portable JDK 21 + fixes Maven SSL)
.\scripts\setup-jdk.ps1

# Build all agents
.\scripts\build.ps1
```

Or manually:

```bash
mvn clean install -DskipTests
```

## Run

```powershell
# Start all 16 services (14 agents + registry + orchestrator)
.\scripts\start-agents.ps1

# Stop all services
.\scripts\stop-agents.ps1
```

Logs are written to `logs/`. Services listen on ports 8401-8414 (agents), 8200 (orchestrator), 8201 (registry).

## API Usage

### Direct agent invocation

```bash
curl -X POST http://localhost:8402/api/v1/agent/process \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "req-001",
    "customerId": "CUST-12345",
    "userMessage": "Show my account balance"
  }'
```

### Orchestrated flow

```bash
curl -X POST http://localhost:8200/api/v1/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "req-002",
    "customerId": "CUST-12345",
    "userMessage": "I need a home loan for 50 lakhs"
  }'
```

### Agent registry

```bash
curl http://localhost:8201/api/v1/registry/agents
```

## Shared Library

All agents depend on `agents/agent-common` which provides:

- `BfsiAgent` interface and `AbstractBfsiAgent` base class
- `AgentRequest` / `AgentResponse` contracts
- BFSI domain models (CustomerProfile, KycVerificationResult, etc.)
- `AgentController` REST base class
