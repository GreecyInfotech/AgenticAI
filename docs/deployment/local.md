# Local Development Guide

Run the platform on your machine without Docker.

## Prerequisites

- Python 3.13+
- Node.js 20+
- Git

## 1. Backend Setup

```powershell
cd ai-distributor-ordering-platform
copy .env.example .env
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
```

## 2. Start API Server

```powershell
$env:PYTHONPATH = ".;ai-platform"
$env:KAFKA_ENABLED = "false"
python -m uvicorn ai_platform.main:app --host 127.0.0.1 --port 8000 --reload
```

The API starts in **degraded mode** without Postgres/Redis/Kafka, using in-memory data.

Verify: http://localhost:8000/api/v1/health

## 3. Start Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open: http://localhost:5173

The Vite dev server proxies `/api` requests to `http://localhost:8000`.

## 4. Login

| Field | Value |
|-------|-------|
| Customer ID | `CUST-001` |
| Role | `distributor` |

## With Infrastructure (Optional)

Start only the databases you need:

```powershell
docker compose up -d postgres redis kafka
```

Update `.env`:

```env
POSTGRES_HOST=localhost
REDIS_HOST=localhost
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_ENABLED=true
```

Restart the API server to connect.

## Development Commands

```bash
make lint        # ruff + black check
make format      # auto-fix formatting
make typecheck   # mypy strict
make test        # pytest with coverage
make run         # uvicorn dev server
```

## IDE Setup

Cursor/VS Code settings are in `.cursor/settings.json`:
- Python interpreter: `.venv/Scripts/python.exe`
- Formatter: Ruff
- Type checking: strict

## Seed Data (In-Memory)

| Resource | ID | Details |
|----------|----|---------|
| Customer | CUST-001 | Demo Distributor, gold tier |
| Product | SKU-001 | Widget A, $29.99 |
| Product | SKU-002 | Widget B, $49.99 |
| Product | SKU-12345 | Industrial Bearing, $15.50 |
| Inventory | SKU-001 | 500 units at WH-01 |

With Postgres running, seed data is loaded from `infrastructure/postgres/init.sql`.

## Related

- [Docker Compose Guide](docker.md)
- [Frontend Guide](../frontend.md)
- [User Manual](../usermanual.md)
