import { useQuery } from '@tanstack/react-query';
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
}