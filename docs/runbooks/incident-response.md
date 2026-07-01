# Incident Response Runbook

Common incidents and remediation steps.

## Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| **P1** | Platform down, no orders possible | Immediate |
| **P2** | Degraded (AI or single service down) | < 30 min |
| **P3** | Non-critical feature impaired | < 4 hours |
| **P4** | Cosmetic / monitoring alert | Next business day |

---

## P1: API Not Responding

**Symptoms:** Health check fails, frontend shows connection error.

**Diagnosis:**
```powershell
curl http://localhost:8000/api/v1/health
docker compose ps
docker compose logs ai-platform --tail 100
```

**Remediation:**
1. Check if port 8000 is in use: `netstat -ano | findstr :8000`
2. Restart API: `docker compose restart ai-platform`
3. If startup hangs, check Postgres/Redis/Kafka connectivity
4. Run without infrastructure: `$env:KAFKA_ENABLED="false"` and restart

---

## P1: Database Connection Failed

**Symptoms:** `postgres_unavailable` in logs, orders not persisting.

**Diagnosis:**
```powershell
docker compose logs postgres --tail 50
docker compose exec postgres pg_isready -U distributor
```

**Remediation:**
1. Verify Postgres is running: `docker compose up -d postgres`
2. Check credentials in `.env` match docker-compose
3. Reset database: `docker compose down -v && docker compose up -d postgres`
4. Platform continues in degraded mode (in-memory) until Postgres recovers

---

## P2: AI Conversation Not Working

**Symptoms:** `/conversation` returns errors or mock responses only.

**Diagnosis:**
```powershell
# Check LLM provider
echo $env:LLM_PROVIDER
echo $env:OPENAI_API_KEY  # Should not be empty for OpenAI
```

**Remediation:**
1. Without API key: responses use MockLLM (expected in dev)
2. Set `OPENAI_API_KEY` in `.env` and restart API
3. For Ollama: ensure `ollama serve` is running, set `LLM_PROVIDER=ollama`
4. Check prompt injection guard isn't blocking legitimate messages

---

## P2: Kafka Events Not Publishing

**Symptoms:** `kafka_event_buffered` in logs, no events in Kafka.

**Diagnosis:**
```powershell
docker compose logs kafka --tail 50
docker compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

**Remediation:**
1. Wait 30-60s for Kafka to fully start
2. Verify `KAFKA_BOOTSTRAP_SERVERS` is correct (localhost:9092 or kafka:9092)
3. Set `KAFKA_ENABLED=false` for dev without Kafka
4. Events are buffered in memory and can be retrieved via `get_buffered_events()`

---

## P2: JWT Authentication Failures

**Symptoms:** 401 on all API calls, frontend redirects to login.

**Remediation:**
1. Verify `JWT_SECRET` hasn't changed between token issuance and validation
2. Check token expiry: default 60 minutes
3. Re-login via frontend or `POST /api/v1/auth/token`
4. Ensure `Authorization: Bearer <token>` header is sent

---

## P3: High LLM Latency

**Symptoms:** Conversation takes > 10 seconds.

**Remediation:**
1. Check OpenAI API status: https://status.openai.com
2. Switch to faster model: `OPENAI_MODEL=gpt-4o-mini`
3. Use local Ollama for development
4. Monitor via Langfuse tracing if configured

---

## P3: Frontend Proxy Errors

**Symptoms:** `ECONNREFUSED` in Vite console.

**Remediation:**
1. Ensure API is running on port 8000
2. Check `frontend/vite.config.ts` proxy target
3. Restart frontend: `cd frontend && npm run dev`
4. Hard refresh browser (Ctrl+Shift+R)

---

## Escalation

If issues persist after remediation:

1. Collect logs: `docker compose logs > incident-logs.txt`
2. Check Grafana dashboards for anomaly timeframe
3. Review recent deployments in CI/CD
4. Roll back to previous Docker image tag

## Related

- [Service Health](service-health.md)
- [Troubleshooting (User Manual)](../usermanual.md#14-troubleshooting)
