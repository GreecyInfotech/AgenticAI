# RAG Platform

Retrieval-Augmented Generation service for all 14 BFSI agents.

## Modules

| Module | Purpose |
|--------|---------|
| `rag-common` | DTOs, RAG context keys, helper utilities |
| `embedding-client` | AI Gateway embedding client with local fallback |
| `vector-store` | In-memory (dev) and pgvector (prod) stores |
| `retrieval-engine` | Ingestion, chunking, hybrid retrieval, knowledge seeding |
| `rag-api` | Deployable service (port **8350**) |

## Features

- **14 agent-scoped knowledge collections** (one per `AgentType`)
- Auto-seeded BFSI regulatory corpus on startup
- Vector similarity + keyword boost hybrid retrieval
- Embeddings via AI Gateway (`/api/v1/embeddings`) with SHA-256 local fallback
- In-memory store for local dev (no Docker required)
- Optional pgvector for production (`RAG_VECTOR_STORE=pgvector`)
- Orchestrator pre-fetches RAG context before domain agent invocation
- All agents attach `ragChunks` and `ragInsight` to responses via `AbstractBfsiAgent`

## Run

```bash
mvn package -DskipTests -pl rag/rag-api -am
java -jar rag/rag-api/target/rag-api-0.1.0-SNAPSHOT.jar
```

Via API Gateway: `POST http://localhost:8000/api/rag/retrieve`

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/retrieve` | Retrieve chunks for an agent |
| POST | `/api/v1/ingest` | Ingest documents into collections |
| GET | `/api/v1/collections` | List all agent collections with counts |
| GET | `/api/v1/health` | Health check |

### Retrieve example

```bash
curl -X POST http://localhost:8350/api/v1/retrieve \
  -H "Content-Type: application/json" \
  -d '{
    "agentType": "LOAN",
    "query": "Am I eligible for a home loan?",
    "topK": 3
  }'
```

### Ingest example

```bash
curl -X POST http://localhost:8350/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [{
      "agentType": "COMPLIANCE",
      "title": "GDPR Update",
      "content": "GDPR Article 33 requires breach notification within 72 hours..."
    }]
  }'
```

## Configuration

```
RAG_PORT=8350
RAG_VECTOR_STORE=memory          # or pgvector
AI_GATEWAY_URL=http://localhost:8300
EMBEDDING_MODEL=text-embedding-3-small
PGVECTOR_HOST=localhost
PGVECTOR_PORT=5433
PGVECTOR_DB=bfsi_vectors
PGVECTOR_USER=bfsi_vector
PGVECTOR_PASSWORD=bfsi_vector_secret
```

## Agent Integration

The orchestrator calls RAG before each domain agent:

```
Intent Agent → resolve target → RAG retrieve → Domain Agent (with ragChunks in context)
```

Each agent response includes:
- `data.ragChunks` — retrieved knowledge chunks with scores
- `data.ragInsight` — top chunk summary for UI display

## Knowledge Collections

| Agent | Collection | Domain |
|-------|------------|--------|
| INTENT | agent-intent | Routing taxonomy |
| CUSTOMER | agent-customer | FAQs, self-service |
| KYC | agent-kyc | RBI KYC Master Direction |
| AML | agent-aml | PMLA, PEP, STR |
| FRAUD | agent-fraud | Fraud patterns |
| LOAN | agent-loan | Fair lending, eligibility |
| UNDERWRITING | agent-underwriting | IRDAI guidelines |
| CLAIM | agent-claim | Claims procedures |
| COMPLIANCE | agent-compliance | Regulatory corpus |
| AUDIT | agent-audit | Audit logging standards |
| RECOMMENDATION | agent-recommendation | Product suitability |
| PORTFOLIO | agent-portfolio | SEBI advisory |
| ESCALATION | agent-escalation | Handoff playbooks |
| NOTIFICATION | agent-notification | Comms templates |
