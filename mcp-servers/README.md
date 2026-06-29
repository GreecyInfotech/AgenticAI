# MCP Servers

HTTP-based MCP-compatible tool servers for BFSI agent integrations.

## Servers

| Server | Port | Tools |
|--------|------|-------|
| core-banking | 8501 | get_account_balance, get_customer_accounts, get_transaction_history, transfer_funds |
| crm | 8502 | get_customer_profile, get_relationship_summary, search_customers |
| postgres | 8503 | log_audit_entry, get_audit_trail, query_records |
| regulatory | 8504 | lookup_regulation, check_compliance, list_frameworks |
| email | 8505 | send_email, send_sms, get_delivery_status |
| jira | 8506 | create_ticket, get_ticket, list_open_tickets |

## Run

```bash
cd mcp-servers
npm install
npm start              # all servers
npm run start:crm      # single server
```

## API

```bash
# List tools
curl http://localhost:8501/tools

# MCP manifest
curl http://localhost:8501/mcp/manifest

# Invoke tool
curl -X POST http://localhost:8501/tools/get_account_balance \
  -H "Content-Type: application/json" \
  -d '{"accountId":"ACC-001"}'
```
