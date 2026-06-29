# BFSI Frontend

Production-ready React frontend for the BFSI Agentic AI Platform.

## Stack

- React 18 + TypeScript
- Vite 6
- Tailwind CSS
- React Router
- TanStack Query

## Portals

| Route | Persona | Features |
|-------|---------|----------|
| `/customer` | Customer | AI chat, session management, agent trail |
| `/employee` | Employee | Staff chat, case escalation |
| `/admin` | Admin | Agent registry, platform health, debug chat |

## Run

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open http://localhost:5173

Requires the backend platform running (`.\scripts\start-all.ps1`).

## Build

```bash
npm run build
npm run preview
```

Production build outputs to `dist/`.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | (empty) | API gateway URL. Empty uses Vite dev proxy to `:8000` |
| `VITE_DEFAULT_CUSTOMER_ID` | `CUST-12345` | Demo customer ID |

For production behind a reverse proxy, set:

```
VITE_API_BASE_URL=https://api.yourbank.com
```

## Docker

```bash
docker build -t bfsi-frontend .
docker run -p 5173:80 bfsi-frontend
```

## API Endpoints Used

All requests go through the API Gateway (`:8000`):

- `POST /api/customer/v1/chat`
- `POST /api/employee/v1/chat`
- `POST /api/employee/v1/cases`
- `GET /api/admin/v1/agents`
- `GET /api/admin/v1/platform/health`
- `POST /api/admin/v1/chat`
