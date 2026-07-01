import { FormEvent, useState } from "react";
import { Navigate } from "react-router-dom";
import { ApiClientError } from "../api/client";
import { useAuth } from "../context/AuthContext";

const ROLES = ["distributor", "sales_rep", "admin", "viewer"] as const;

export default function LoginPage() {
  const { user, login } = useAuth();
  const [subject, setSubject] = useState("CUST-001");
  const [role, setRole] = useState<string>("distributor");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/" replace />;

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(subject.trim(), role);
    } catch (err) {
      setError(err instanceof ApiClientError ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <span className="brand-icon lg">AI</span>
          <h1>Distributor Ordering</h1>
          <p>Sign in to access the AI-powered ordering platform</p>
        </div>
        <form onSubmit={handleSubmit} className="login-form">
          <label>
            Customer ID
            <input
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="CUST-001"
              required
            />
          </label>
          <label>
            Role
            <select value={role} onChange={(e) => setRole(e.target.value)}>
              {ROLES.map((r) => (
                <option key={r} value={r}>
                  {r.replace("_", " ")}
                </option>
              ))}
            </select>
          </label>
          {error && <div className="alert error">{error}</div>}
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <p className="login-hint">
          Demo account: <code>CUST-001</code> as <code>distributor</code>
        </p>
      </div>
    </div>
  );
}
