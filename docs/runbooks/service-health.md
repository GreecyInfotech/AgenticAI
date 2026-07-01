# Service Health Runbook

Monitoring and health check procedures for all platform services.

## Health Endpoints

Every service exposes:

| Endpoint | Purpose | Expected |
|----------|---------|----------|
| `/health` | Liveness | `{"status": "UP"}` |
| `/ready` | Readiness | `{"status": "READY"}` or `503` |
| `/metrics` | Prometheus | text/plain metrics |

AI Platform additionally exposes `/api/v1/health` and `/api/v1/ready`.

## Quick Health Check

```powershell
# AI Platform
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/ready

# Gateway
curl http://localhost:8080/health
curl http://localhost:8080/ready

# Microservices (example)
curl http://localhost:8001/health
curl http://localhost:8002/health
```

## Dependency Status

AI Platform `/api/v1/ready` reports dependency health:

```json
{
  "status": "READY",
  "dependencies": {
    "postgres": {"status": "UP"},
    "redis": {"status": "DOWN", "detail": "client not initialized"}
  }
}
```

| Dependency Status | Platform Behavior |
|-------------------|-------------------|
| Postgres UP | Repositories use database |
| Postgres DOWN | In-memory fallback with seed data |
| Redis UP | Session memory in Redis |
| Redis DOWN | In-memory session store |
| Kafka UP | Events published to topics |
| Kafka DOWN | Events buffered in memory |

## Prometheus Metrics

Scrape targets configured in `infrastructure/monitoring/prometheus.yml`:

| Job | Target | Path |
|-----|--------|------|
| ai-platform | ai-platform:8000 | /api/v1/metrics |
| gateway | gateway:8080 | /metrics |
| microservices | order/inventory/customer/payment:8080 | /metrics |

Access Prometheus UI: http://localhost:9090

## Key Metrics to Monitor

| Metric | Alert Threshold | Action |
|--------|----------------|--------|
| HTTP 5xx rate | > 1% over 5 min | Check logs, restart service |
| Request latency p99 | > 5s | Check LLM/DB latency |
| Kafka consumer lag | > 1000 messages | Scale consumers |
| Postgres connections | > 80% pool | Increase pool size |
| Redis memory | > 80% | Review TTL policies |
| LLM API errors | > 5% | Check API key, rate limits |

## Docker Health Checks

```powershell
docker compose ps                    # All services status
docker compose logs ai-platform      # API logs
docker compose logs kafka --tail 50  # Kafka startup
```

## Startup Timeouts

Infrastructure connections have 5-second timeouts during startup (`app/lifespan.py`). If a dependency is slow to start:

1. Check Docker container health: `docker compose ps`
2. Wait for Postgres/Kafka to be healthy before API starts
3. Use `depends_on` with `condition: service_healthy` in docker-compose

## Grafana Dashboards

Access: http://localhost:3000 (admin/admin)

Recommended dashboards to import:
- FastAPI Observability
- Kafka Overview
- PostgreSQL Database
- Node Exporter (if deployed)

## Related

- [Incident Response](incident-response.md)
- [Production Deployment](../deployment/production.md)
