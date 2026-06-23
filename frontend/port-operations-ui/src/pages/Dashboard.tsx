import { useQuery } from '@tanstack/react-query';
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
}