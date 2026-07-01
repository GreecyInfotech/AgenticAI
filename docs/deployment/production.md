# Production Deployment Checklist

Guidelines for deploying the AI Distributor Ordering Platform to production.

## Pre-Deployment Checklist

### Security

- [ ] Change `JWT_SECRET` to a cryptographically random 64+ character string
- [ ] Set strong `POSTGRES_PASSWORD` (not the default)
- [ ] Configure `OPENAI_API_KEY` or Azure OpenAI credentials
- [ ] Replace `/auth/token` dev endpoint with OAuth 2.0 / Okta
- [ ] Enable TLS termination (nginx or cloud load balancer)
- [ ] Restrict CORS origins to production frontend domain
- [ ] Review RBAC role assignments for production users
- [ ] Enable prompt injection guards (enabled by default)
- [ ] Verify PII masking in logs

### Infrastructure

- [ ] Deploy PostgreSQL with backups and replication
- [ ] Deploy Redis for session memory and idempotency
- [ ] Deploy Kafka cluster with appropriate replication factor
- [ ] Deploy Qdrant for RAG knowledge base
- [ ] Configure Kafka topic creation (see `infrastructure/kafka/topics.txt`)
- [ ] Set up database migrations (Alembic recommended)
- [ ] Configure Redis-backed idempotency store (replace in-memory)

### Application

- [ ] Set `APP_ENV=production`
- [ ] Set `LOG_LEVEL=INFO` or `WARNING`
- [ ] Set `KAFKA_ENABLED=true`
- [ ] Configure `OTEL_ENABLED=true` with collector endpoint
- [ ] Build and push Docker images to container registry
- [ ] Deploy via Kubernetes (`infrastructure/kubernetes/`) or Helm (`infrastructure/helm/`)
- [ ] Provision cloud resources with Terraform (`infrastructure/terraform/`)

### Observability

- [ ] Configure Prometheus scraping for all services
- [ ] Import Grafana dashboards
- [ ] Set up alerting rules (API latency, error rate, Kafka lag)
- [ ] Enable OpenTelemetry distributed tracing
- [ ] Configure Langfuse for LLM call tracing (optional)
- [ ] Set up log aggregation (ELK, Loki, or cloud logging)

### Testing

- [ ] Run full test suite: `make test`
- [ ] Run contract tests: `pytest tests/contract`
- [ ] Run security tests: `pytest tests/security`
- [ ] Perform load testing: `tests/load/`
- [ ] Validate all health/ready endpoints

## Environment Variables (Production)

```env
APP_ENV=production
LOG_LEVEL=INFO

# Use managed database
POSTGRES_HOST=prod-db.example.com
POSTGRES_PASSWORD=<strong-password>

# Use managed Redis
REDIS_HOST=prod-redis.example.com

# Use managed Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka-1:9092,kafka-2:9092,kafka-3:9092
KAFKA_ENABLED=true

# Security
JWT_SECRET=<64-char-random-string>
JWT_EXPIRE_MINUTES=30

# LLM
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Observability
OTEL_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=https://otel-collector.example.com:4317
```

## Scaling Guidelines

| Component | Scaling Strategy |
|-----------|-----------------|
| AI Platform | Horizontal (stateless API, session in Redis) |
| Gateway | Horizontal behind load balancer |
| Microservices | Independent per-domain scaling |
| Postgres | Vertical + read replicas |
| Kafka | Partition by topic, increase replication |
| Qdrant | Shard collections by domain |
| Redis | Cluster mode for HA |

## CI/CD

GitHub Actions workflows in `.github/workflows/`:

| Workflow | Trigger | Action |
|----------|---------|--------|
| `lint.yml` | Push, PR | Ruff + Black |
| `tests.yml` | Push, PR | pytest |
| `docker.yml` | Push to main | Build AI platform image |
| `security.yml` | Push, PR | Security scanning |
| `deploy-dev.yml` | Push to develop | Deploy to dev |
| `deploy-stage.yml` | Push to staging | Deploy to staging |
| `deploy-prod.yml` | Push to main | Deploy to production |

## Rollback

1. Revert to previous Docker image tag
2. Run database migration rollback if schema changed
3. Verify health endpoints
4. Monitor error rates in Grafana

## Related

- [Docker Compose](docker.md) — local full stack
- [Service Health Runbook](../runbooks/service-health.md)
- [Incident Response](../runbooks/incident-response.md)
