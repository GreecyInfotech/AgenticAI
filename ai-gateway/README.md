# AI Gateway

Production-ready LLM gateway for the BFSI Agentic AI Platform.

## Modules

| Module | Purpose |
|--------|---------|
| `ai-gateway-common` | Shared DTOs, contracts, exceptions |
| `provider-adapters` | OpenAI, Azure OpenAI, Mock providers |
| `prompt-router` | BFSI prompt templates per agent |
| `token-manager` | Token budget enforcement and usage tracking |
| `response-cache` | Redis-backed response cache (in-memory fallback) |
| `model-router` | Main service (port 8300) |

## Features

- Multi-provider routing (OpenAI, Azure OpenAI, Mock fallback)
- Agent-aware model selection (KYC/AML → gpt-4o, Intent → gpt-4o-mini)
- BFSI prompt templates with variable substitution
- Token budget per request and session
- Response caching (Redis or in-memory)
- Guardrails: PII detection (PAN, Aadhaar), prompt injection blocking
- Prometheus metrics via Actuator

## Run

```bash
# Local dev (mock provider, in-memory cache)
mvn -pl ai-gateway/model-router spring-boot:run -Dspring-boot.run.profiles=dev

# Production profile (requires API keys; optional Redis)
mvn -pl ai-gateway/model-router spring-boot:run -Dspring-boot.run.profiles=prod

# Fat JAR
mvn package -DskipTests -pl ai-gateway/model-router -am
java -jar ai-gateway/model-router/target/model-router-0.1.0-SNAPSHOT.jar --spring.profiles.active=prod
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat/completions` | Chat completion |
| POST | `/api/v1/embeddings` | Text embeddings |
| GET | `/api/v1/models` | List available models |
| GET | `/api/v1/prompts` | List prompt templates |
| GET | `/api/v1/prompts/{id}` | Get prompt template |
| GET | `/api/v1/usage` | Token usage stats |
| GET | `/api/v1/health` | Health check |

Via API Gateway: `http://localhost:8000/api/ai/chat/completions`

## Example

```bash
curl -X POST http://localhost:8300/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "req-001",
    "agentType": "LOAN",
    "customerId": "CUST-12345",
    "messages": [{"role": "user", "content": "Am I eligible for a home loan?"}],
    "promptVariables": {"customerId": "CUST-12345", "amount": "5000000"}
  }'
```

## Configuration

Set in `.env` or environment:

```
OPENAI_API_KEY=sk-...
AZURE_OPENAI_ENDPOINT=https://....openai.azure.com
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT=gpt-4o
DEFAULT_LLM_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_ENABLED=true
AI_GATEWAY_PORT=8300
```

Without API keys, the gateway uses the **Mock provider** for local development (`ai.routing.allow-mock: true` in dev profile).

Production (`spring.profiles.active=prod`):
- Mock provider disabled
- Redis cache enabled when `REDIS_ENABLED=true`
- Requires `OPENAI_API_KEY` or Azure OpenAI configuration
