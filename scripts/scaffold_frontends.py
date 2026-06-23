#!/usr/bin/env python3
"""Scaffold frontend React/Vite applications."""

from pathlib import Path

ROOT = Path(__file__).parent.parent

FRONTENDS = {
    "port-operations-ui": {
        "title": "Port Operations",
        "port": 5173,
        "description": "Real-time port operations control center",
        "theme": "#1e40af",
    },
    "executive-dashboard": {
        "title": "Executive Dashboard",
        "port": 5174,
        "description": "Executive KPI and strategic analytics dashboard",
        "theme": "#059669",
    },
    "customs-dashboard": {
        "title": "Customs Dashboard",
        "port": 5175,
        "description": "Customs clearance and compliance monitoring",
        "theme": "#7c3aed",
    },
    "mobile-app": {
        "title": "Smart Port Mobile",
        "port": 5176,
        "description": "Mobile field operations app",
        "theme": "#dc2626",
    },
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def scaffold_frontend(name: str, cfg: dict) -> None:
    base = ROOT / "frontend" / name
    write(base / "package.json", f'''{{
  "name": "{name}",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {{
    "dev": "vite --port {cfg['port']}",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src/"
  }},
  "dependencies": {{
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.26.0",
    "@tanstack/react-query": "^5.56.0",
    "axios": "^1.7.0",
    "recharts": "^2.12.0",
    "lucide-react": "^0.441.0",
    "smart-port-types": "workspace:*"
  }},
  "devDependencies": {{
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "typescript": "^5.5.0",
    "vite": "^5.4.0"
  }}
}}''')

    write(base / "tsconfig.json", '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true
  },
  "include": ["src"]
}''')

    write(base / "vite.config.ts", f'''import {{ defineConfig }} from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({{
  plugins: [react()],
  server: {{ port: {cfg['port']}, proxy: {{ '/api': 'http://localhost:8080' }} }},
}});
''')

    write(base / "index.html", f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{cfg['title']} | Smart Port AI</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
''')

    write(base / "src" / "main.tsx", '''import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App';
import './index.css';

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
);
''')

    write(base / "src" / "index.css", f'''*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --primary: {cfg['theme']};
  --bg: #0f172a;
  --surface: #1e293b;
  --text: #f1f5f9;
  --muted: #94a3b8;
  --border: #334155;
}}
body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); }}
''')

    write(base / "src" / "App.tsx", f'''import {{ BrowserRouter, Routes, Route, Navigate }} from 'react-router-dom';
import {{ Layout }} from './components/Layout';
import {{ Dashboard }} from './pages/Dashboard';
import {{ Login }} from './pages/Login';
import {{ useAuth }} from './hooks/useAuth';

export default function App() {{
  const {{ isAuthenticated }} = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={{<Login />}} />
        <Route path="/" element={{isAuthenticated ? <Layout /> : <Navigate to="/login" />}}>
          <Route index element={{<Dashboard />}} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}}
''')

    write(base / "src" / "hooks" / "useAuth.ts", '''import { useState, useCallback } from 'react';
import axios from 'axios';

const TOKEN_KEY = 'smart_port_token';

export function useAuth() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY));

  const login = useCallback(async (username: string, password: string) => {
    const { data } = await axios.post('/api/v1/auth/login', { username, password });
    localStorage.setItem(TOKEN_KEY, data.access_token);
    setToken(data.access_token);
    return data;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
  }, []);

  return { token, isAuthenticated: !!token, login, logout };
}
''')

    write(base / "src" / "api" / "client.ts", '''import axios from 'axios';

const TOKEN_KEY = 'smart_port_token';

export const api = axios.create({ baseURL: '/api/v1' });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
''')

    write(base / "src" / "components" / "Layout.tsx", f'''import {{ Outlet, Link }} from 'react-router-dom';
import {{ useAuth }} from '../hooks/useAuth';

export function Layout() {{
  const {{ logout }} = useAuth();

  return (
    <div style={{{{ display: 'flex', minHeight: '100vh' }}}}>
      <nav style={{{{ width: 240, background: 'var(--surface)', padding: '1.5rem', borderRight: '1px solid var(--border)' }}}}>
        <h2 style={{{{ color: 'var(--primary)', marginBottom: '2rem', fontSize: '1.1rem' }}}}>
          {cfg['title']}
        </h2>
        <Link to="/" style={{{{ color: 'var(--text)', textDecoration: 'none', display: 'block', padding: '0.5rem 0' }}}}>
          Dashboard
        </Link>
        <button onClick={{logout}} style={{{{ marginTop: '2rem', background: 'var(--primary)', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: 6, cursor: 'pointer' }}}}>
          Logout
        </button>
      </nav>
      <main style={{{{ flex: 1, padding: '2rem' }}}}>
        <Outlet />
      </main>
    </div>
  );
}}
''')

    write(base / "src" / "pages" / "Login.tsx", f'''import {{ useState }} from 'react';
import {{ useNavigate }} from 'react-router-dom';
import {{ useAuth }} from '../hooks/useAuth';

export function Login() {{
  const [username, setUsername] = useState('operator');
  const [password, setPassword] = useState('operator');
  const [error, setError] = useState('');
  const {{ login }} = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault();
    try {{
      await login(username, password);
      navigate('/');
    }} catch {{
      setError('Invalid credentials');
    }}
  }};

  return (
    <div style={{{{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}}}>
      <form onSubmit={{handleSubmit}} style={{{{ background: 'var(--surface)', padding: '2rem', borderRadius: 12, width: 360 }}}}>
        <h1 style={{{{ marginBottom: '0.5rem', color: 'var(--primary)' }}}}>Smart Port AI</h1>
        <p style={{{{ color: 'var(--muted)', marginBottom: '1.5rem', fontSize: '0.9rem' }}}}>{cfg['description']}</p>
        {{error && <p style={{{{ color: '#ef4444', marginBottom: '1rem' }}}}>{{error}}</p>}}
        <input value={{username}} onChange={{e => setUsername(e.target.value)}} placeholder="Username"
          style={{{{ width: '100%', padding: '0.75rem', marginBottom: '1rem', background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 6, color: 'var(--text)' }}}} />
        <input type="password" value={{password}} onChange={{e => setPassword(e.target.value)}} placeholder="Password"
          style={{{{ width: '100%', padding: '0.75rem', marginBottom: '1.5rem', background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 6, color: 'var(--text)' }}}} />
        <button type="submit" style={{{{ width: '100%', padding: '0.75rem', background: 'var(--primary)', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontWeight: 600 }}}}>
          Sign In
        </button>
      </form>
    </div>
  );
}}
''')

    # Dashboard varies by app
    if name == "executive-dashboard":
        dashboard_content = '''import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { api } from '../api/client';

export function Dashboard() {
  const { data: kpis } = useQuery({
    queryKey: ['executive-kpis'],
    queryFn: () => api.get('/analytics/dashboard/executive').then(r => r.data),
  });

  const revenueData = kpis?.trends?.revenue?.map((v: number, i: number) => ({ month: `M${i+1}`, revenue: v })) || [];

  return (
    <div>
      <h1 style={{ marginBottom: '1.5rem' }}>Executive Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
        {Object.entries(kpis?.kpis || {}).map(([key, value]) => (
          <div key={key} style={{ background: 'var(--surface)', padding: '1.5rem', borderRadius: 8, border: '1px solid var(--border)' }}>
            <p style={{ color: 'var(--muted)', fontSize: '0.85rem', textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}</p>
            <p style={{ fontSize: '1.5rem', fontWeight: 700, marginTop: '0.5rem' }}>{typeof value === 'number' ? value.toLocaleString() : value}</p>
          </div>
        ))}
      </div>
      <div style={{ background: 'var(--surface)', padding: '1.5rem', borderRadius: 8, border: '1px solid var(--border)' }}>
        <h3 style={{ marginBottom: '1rem' }}>Revenue Trend (M USD)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={revenueData}>
            <XAxis dataKey="month" stroke="var(--muted)" />
            <YAxis stroke="var(--muted)" />
            <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)' }} />
            <Line type="monotone" dataKey="revenue" stroke="var(--primary)" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}'''
    elif name == "customs-dashboard":
        dashboard_content = '''import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';

export function Dashboard() {
  const { data: declarations } = useQuery({
    queryKey: ['customs-declarations'],
    queryFn: () => api.get('/customs/declarations').then(r => r.data),
  });
  const { data: queue } = useQuery({
    queryKey: ['customs-queue'],
    queryFn: () => api.get('/customs/clearance-queue').then(r => r.data),
  });

  return (
    <div>
      <h1 style={{ marginBottom: '1.5rem' }}>Customs Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
        {queue && Object.entries(queue).map(([key, value]) => (
          <div key={key} style={{ background: 'var(--surface)', padding: '1.5rem', borderRadius: 8, border: '1px solid var(--border)' }}>
            <p style={{ color: 'var(--muted)', fontSize: '0.85rem', textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}</p>
            <p style={{ fontSize: '2rem', fontWeight: 700 }}>{value as number}</p>
          </div>
        ))}
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid var(--border)' }}>
            {['ID', 'Vessel', 'Status', 'Risk Score'].map(h => (
              <th key={h} style={{ textAlign: 'left', padding: '0.75rem', color: 'var(--muted)' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {declarations?.data?.map((d: { id: string; vessel: string; status: string; risk_score: number }) => (
            <tr key={d.id} style={{ borderBottom: '1px solid var(--border)' }}>
              <td style={{ padding: '0.75rem' }}>{d.id}</td>
              <td style={{ padding: '0.75rem' }}>{d.vessel}</td>
              <td style={{ padding: '0.75rem' }}>{d.status}</td>
              <td style={{ padding: '0.75rem', color: d.risk_score > 0.5 ? '#ef4444' : '#22c55e' }}>{(d.risk_score * 100).toFixed(0)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}'''
    else:
        dashboard_content = '''import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';

export function Dashboard() {
  const { data: vessels } = useQuery({
    queryKey: ['vessels'],
    queryFn: () => api.get('/vessels').then(r => r.data),
  });
  const { data: yard } = useQuery({
    queryKey: ['yard-status'],
    queryFn: () => api.get('/containers/yard-status').then(r => r.data),
  });

  return (
    <div>
      <h1 style={{ marginBottom: '1.5rem' }}>Operations Dashboard</h1>
      {yard && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
          <div style={{ background: 'var(--surface)', padding: '1.5rem', borderRadius: 8, border: '1px solid var(--border)' }}>
            <p style={{ color: 'var(--muted)' }}>Yard Utilization</p>
            <p style={{ fontSize: '2rem', fontWeight: 700 }}>{(yard.utilization * 100).toFixed(0)}%</p>
          </div>
          <div style={{ background: 'var(--surface)', padding: '1.5rem', borderRadius: 8, border: '1px solid var(--border)' }}>
            <p style={{ color: 'var(--muted)' }}>Occupied Slots</p>
            <p style={{ fontSize: '2rem', fontWeight: 700 }}>{yard.occupied?.toLocaleString()}</p>
          </div>
          <div style={{ background: 'var(--surface)', padding: '1.5rem', borderRadius: 8, border: '1px solid var(--border)' }}>
            <p style={{ color: 'var(--muted)' }}>Available</p>
            <p style={{ fontSize: '2rem', fontWeight: 700 }}>{yard.available?.toLocaleString()}</p>
          </div>
          <div style={{ background: 'var(--surface)', padding: '1.5rem', borderRadius: 8, border: '1px solid var(--border)' }}>
            <p style={{ color: 'var(--muted)' }}>Active Vessels</p>
            <p style={{ fontSize: '2rem', fontWeight: 700 }}>{vessels?.total || 0}</p>
          </div>
        </div>
      )}
      <h2 style={{ marginBottom: '1rem' }}>Vessel Schedule</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid var(--border)' }}>
            {['Vessel', 'ETA', 'Berth', 'Status'].map(h => (
              <th key={h} style={{ textAlign: 'left', padding: '0.75rem', color: 'var(--muted)' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {vessels?.data?.map((v: { id: string; name: string; eta: string; berth: string; status: string }) => (
            <tr key={v.id} style={{ borderBottom: '1px solid var(--border)' }}>
              <td style={{ padding: '0.75rem' }}>{v.name}</td>
              <td style={{ padding: '0.75rem' }}>{new Date(v.eta).toLocaleString()}</td>
              <td style={{ padding: '0.75rem' }}>{v.berth}</td>
              <td style={{ padding: '0.75rem' }}>{v.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}'''

    write(base / "src" / "pages" / "Dashboard.tsx", dashboard_content)

    write(base / "Dockerfile", f'''FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml ./
COPY frontend/{name}/package.json ./frontend/{name}/
COPY shared/typescript/smart-port-types/package.json ./shared/typescript/smart-port-types/
RUN pnpm install --filter {name}...
COPY frontend/{name} ./frontend/{name}
COPY shared/typescript/smart-port-types ./shared/typescript/smart-port-types
RUN pnpm --filter {name} build

FROM nginx:alpine
COPY --from=builder /app/frontend/{name}/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
''')


if __name__ == "__main__":
    for name, cfg in FRONTENDS.items():
        scaffold_frontend(name, cfg)
    print("Scaffolded all frontend apps.")
