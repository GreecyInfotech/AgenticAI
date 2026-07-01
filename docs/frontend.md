# Frontend Guide

React web application for the AI Distributor Ordering Platform.

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 19 | UI framework |
| TypeScript | 5.7 | Type safety |
| Vite | 6 | Build tool + dev server |
| React Router | 7 | Client-side routing |

## Project Structure

```
frontend/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── .env.example
├── src/
│   ├── main.tsx              # App entry point
│   ├── App.tsx               # Routes definition
│   ├── api/
│   │   └── client.ts         # API client with JWT auth
│   ├── context/
│   │   └── AuthContext.tsx    # Auth state management
│   ├── components/
│   │   └── Layout.tsx        # Sidebar + navigation
│   ├── pages/
│   │   ├── LoginPage.tsx     # JWT login
│   │   ├── DashboardPage.tsx # Overview + quick actions
│   │   ├── ConversationPage.tsx # AI chat interface
│   │   ├── OrdersPage.tsx    # Create + list orders
│   │   ├── ProductsPage.tsx  # Product catalog
│   │   └── InventoryPage.tsx # Stock lookup
│   └── styles/
│       └── index.css         # Dark theme design system
└── dist/                     # Production build output
```

## Getting Started

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Pages

| Route | Page | Description |
|-------|------|-------------|
| `/login` | Login | JWT authentication |
| `/` | Dashboard | API status, stats, quick actions |
| `/conversation` | AI Assistant | LangGraph chat with agent routing |
| `/orders` | Orders | Create orders + view history |
| `/products` | Products | Browse product catalog |
| `/inventory` | Inventory | Check stock by SKU |

## Authentication Flow

1. User enters Customer ID and Role on login page
2. Frontend calls `POST /api/v1/auth/token`
3. JWT stored in `localStorage`
4. All API requests include `Authorization: Bearer {token}`
5. Protected routes redirect to `/login` if unauthenticated

## API Proxy

During development, Vite proxies `/api` to the backend:

```typescript
// vite.config.ts
proxy: {
  "/api": {
    target: "http://localhost:8000",  // or 8080 for gateway
    changeOrigin: true,
  },
}
```

Set `VITE_PROXY_TARGET` in `.env` to change the target.

## Environment Variables

```env
VITE_API_URL=              # Leave empty to use Vite proxy
VITE_PROXY_TARGET=http://localhost:8000
```

## Production Build

```powershell
npm run build     # Output to dist/
npm run preview   # Preview production build
```

Docker:

```powershell
docker build -f infrastructure/docker/Dockerfile.frontend -t frontend:latest .
```

Served via nginx on port 80 (mapped to 5173 in docker-compose).

## Design System

Dark theme with CSS custom properties:

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | #0c0f14 | Page background |
| `--bg-card` | #1a222d | Card surfaces |
| `--accent` | #3b82f6 | Primary actions, links |
| `--text` | #e8edf4 | Primary text |
| `--text-muted` | #8b9cb3 | Secondary text |
| `--success` | #22c55e | Status badges |
| `--danger` | #ef4444 | Error states |

Font: DM Sans (UI), JetBrains Mono (code/SKUs)

## Demo Credentials

| Field | Value |
|-------|-------|
| Customer ID | CUST-001 |
| Role | distributor |

## Related

- [REST API](../api/rest-api.md)
- [Authentication](../api/authentication.md)
- [Local Development](../deployment/local.md)
