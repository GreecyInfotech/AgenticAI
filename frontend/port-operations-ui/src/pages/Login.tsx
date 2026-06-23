import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function Login() {
  const [username, setUsername] = useState('operator');
  const [password, setPassword] = useState('operator');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate('/');
    } catch {
      setError('Invalid credentials');
    }
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
      <form onSubmit={handleSubmit} style={{ background: 'var(--surface)', padding: '2rem', borderRadius: 12, width: 360 }}>
        <h1 style={{ marginBottom: '0.5rem', color: 'var(--primary)' }}>Smart Port AI</h1>
        <p style={{ color: 'var(--muted)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>Real-time port operations control center</p>
        {error && <p style={{ color: '#ef4444', marginBottom: '1rem' }}>{error}</p>}
        <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username"
          style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem', background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 6, color: 'var(--text)' }} />
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password"
          style={{ width: '100%', padding: '0.75rem', marginBottom: '1.5rem', background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 6, color: 'var(--text)' }} />
        <button type="submit" style={{ width: '100%', padding: '0.75rem', background: 'var(--primary)', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer', fontWeight: 600 }}>
          Sign In
        </button>
      </form>
    </div>
  );
}
