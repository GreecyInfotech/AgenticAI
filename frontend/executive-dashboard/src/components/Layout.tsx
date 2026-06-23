import { Outlet, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function Layout() {
  const { logout } = useAuth();

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <nav style={{ width: 240, background: 'var(--surface)', padding: '1.5rem', borderRight: '1px solid var(--border)' }}>
        <h2 style={{ color: 'var(--primary)', marginBottom: '2rem', fontSize: '1.1rem' }}>
          Executive Dashboard
        </h2>
        <Link to="/" style={{ color: 'var(--text)', textDecoration: 'none', display: 'block', padding: '0.5rem 0' }}>
          Dashboard
        </Link>
        <button onClick={logout} style={{ marginTop: '2rem', background: 'var(--primary)', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: 6, cursor: 'pointer' }}>
          Logout
        </button>
      </nav>
      <main style={{ flex: 1, padding: '2rem' }}>
        <Outlet />
      </main>
    </div>
  );
}
