import { useQuery } from '@tanstack/react-query';
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
}