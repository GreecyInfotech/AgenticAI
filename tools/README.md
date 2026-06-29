# Tools Platform

Production-ready Java SDK and registry service for MCP tool invocation across all BFSI agents.

## Modules

| Module | Purpose |
|--------|---------|
| `tools-common` | Contracts: `ToolExecutor`, `ToolInvocationResult`, manifests |
| `tool-client` | HTTP client for MCP servers (`mcp-http-tools/1.0`) |
| `tool-bindings` | Typed facades per domain + Spring Boot auto-config |
| `tools-api` | Tool registry and proxy service (port **8450**) |

## MCP Tool Servers (19 tools)

| Server | Port | Tools |
|--------|------|-------|
| core-banking | 8501 | `get_account_balance`, `get_customer_accounts`, `get_transaction_history`, `transfer_funds` |
| crm | 8502 | `get_customer_profile`, `get_relationship_summary`, `search_customers` |
| postgres | 8503 | `log_audit_entry`, `get_audit_trail`, `query_records` |
| regulatory | 8504 | `lookup_regulation`, `check_compliance`, `list_frameworks` |
| email | 8505 | `send_email`, `send_sms`, `get_delivery_status` |
| jira | 8506 | `create_ticket`, `get_ticket`, `list_open_tickets` |

## Agent Integration

`tool-bindings` is included via `agent-common`. Agents auto-wire typed tool facades:

| Agent | Tools Used |
|-------|------------|
| Customer | `CrmTools`, `CoreBankingTools` |
| Audit | `AuditTools` |
| Compliance | `RegulatoryTools` |
| Notification | `NotificationTools` |
| Escalation | `EscalationTools` |

Agent responses include `data.toolInvocations` with server, tool name, latency, and result.

## Run

```bash
# Start MCP servers (required)
cd mcp-servers && npm start

# Build and run tools API
mvn package -DskipTests -pl tools/tools-api -am
java -jar tools/tools-api/target/tools-api-0.1.0-SNAPSHOT.jar
```

Via API Gateway: `GET http://localhost:8000/api/tools/tools`

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health + MCP server status |
| GET | `/api/v1/tools` | List all tools across servers |
| GET | `/api/v1/servers` | Discover MCP server manifests |
| POST | `/api/v1/invoke` | Invoke any tool |

### Invoke example

```bash
curl -X POST http://localhost:8450/api/v1/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "serverId": "crm",
    "toolName": "get_customer_profile",
    "arguments": { "customerId": "CUST-12345" }
  }'
```

## Configuration

```yaml
tools:
  mcp:
    enabled: true
    timeout-seconds: 15
    servers:
      core-banking: http://localhost:8501
      crm: http://localhost:8502
      postgres: http://localhost:8503
      regulatory: http://localhost:8504
      email: http://localhost:8505
      jira: http://localhost:8506
```

Set `tools.mcp.enabled: false` to disable tool calls (agents use local fallback).
