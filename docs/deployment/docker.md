# Docker Compose Deployment

Run the complete platform stack with a single command.

## Quick Start

```powershell
copy .env.example .env
docker compose up -d
```

## Services

| Service | Container Port | Host Port | Description |
|---------|---------------|-----------|-------------|
| postgres | 5432 | 5432 | PostgreSQL 16 with seed data |
| redis | 6379 | 6379 | Redis 7 cache |
| qdrant | 6333 | 6333 | Vector database for RAG |
| zookeeper | 2181 | 2181 | Kafka coordination |
| kafka | 9092 | 9092 | Event bus |
| ai-platform | 8000 | 8000 | AI Platform API |
| gateway | 8080 | 8080 | API Gateway |
| order-service | 8080 | 8001 | Order microservice |
| inventory-service | 8080 | 8002 | Inventory microservice |
| customer-service | 8080 | 8003 | Customer microservice |
| pricing-service | 8080 | 8004 | Pricing microservice |
| payment-service | 8080 | 8005 | Payment microservice |
| shipment-service | 8080 | 8006 | Shipment microservice |
| promotion-service | 8080 | 8007 | Promotion microservice |
| notification-service | 8080 | 8008 | Notification microservice |
| analytics-service | 8080 | 8009 | Analytics microservice |
| frontend | 80 | 5173 | React web app (nginx) |
| prometheus | 9090 | 9090 | Metrics collection |
| grafana | 3000 | 3000 | Dashboards |

## Verify

```powershell
# Check all containers
docker compose ps

# API health
curl http://localhost:8000/api/v1/health

# Gateway health
curl http://localhost:8080/health

# Frontend
start http://localhost:5173
```

## Build Images

```powershell
# AI Platform only
docker build -f infrastructure/docker/Dockerfile.ai-platform -t ai-platform:latest .

# Gateway
docker build -f infrastructure/docker/Dockerfile.gateway -t gateway:latest .

# Any microservice
docker build -f infrastructure/docker/Dockerfile.service --build-arg SERVICE_DIR=services/order-service -t order-service:latest .

# Frontend
docker build -f infrastructure/docker/Dockerfile.frontend -t frontend:latest .
```

## Logs

```powershell
docker compose logs -f ai-platform
docker compose logs -f gateway
docker compose logs -f order-service
```

## Stop

```powershell
docker compose down          # Stop containers
docker compose down -v       # Stop + remove volumes (destroys data)
```

## Environment Variables

Key variables for Docker (set in `.env`):

```env
POSTGRES_USER=distributor
POSTGRES_PASSWORD=distributor_secret
POSTGRES_DB=distributor_platform
JWT_SECRET=your-production-secret-here
OPENAI_API_KEY=sk-...
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
AI_PLATFORM_URL=http://ai-platform:8000
```

Inside Docker, services use container names as hostnames (e.g., `postgres`, `redis`, `kafka`).

## PostgreSQL Init

Schema and seed data are loaded automatically from `infrastructure/postgres/init.sql` on first startup.

## Monitoring

- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (default login: admin/admin)

Prometheus scrapes:
- `ai-platform:8000/api/v1/metrics`
- `gateway:8080/metrics`
- Microservices on `/metrics`

## Related

- [Local Development](local.md)
- [Production Deployment](production.md)
