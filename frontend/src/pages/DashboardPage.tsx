import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function DashboardPage() {
  const { user } = useAuth();
  const [health, setHealth] = useState<string>("checking…");
  const [customer, setCustomer] = useState<{ name: string; tier: string } | null>(null);
  const [orderCount, setOrderCount] = useState(0);
  const [productCount, setProductCount] = useState(0);

  useEffect(() => {
    api.health().then((h) => setHealth(h.status)).catch(() => setHealth("DOWN"));
    if (user) {
      api.getCustomer(user.subject).then((c) => setCustomer({ name: c.name, tier: c.tier })).catch(() => null);
      api.listOrders().then((o) => setOrderCount(o.items.length)).catch(() => null);
      api.listProducts().then((p) => setProductCount(p.items.length)).catch(() => null);
    }
  }, [user]);

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>Welcome back{customer ? `, ${customer.name}` : ""}</p>
        </div>
        <span className={`status-badge ${health === "UP" ? "up" : "down"}`}>
          API {health}
        </span>
      </header>

      <div className="stat-grid">
        <div className="stat-card">
          <span className="stat-label">Customer</span>
          <span className="stat-value">{user?.subject}</span>
          {customer && <span className="stat-meta">{customer.tier} tier</span>}
        </div>
        <div className="stat-card">
          <span className="stat-label">Orders</span>
          <span className="stat-value">{orderCount}</span>
          <Link to="/orders" className="stat-link">View orders →</Link>
        </div>
        <div className="stat-card">
          <span className="stat-label">Products</span>
          <span className="stat-value">{productCount}</span>
          <Link to="/products" className="stat-link">Browse catalog →</Link>
        </div>
        <div className="stat-card accent">
          <span className="stat-label">AI Assistant</span>
          <span className="stat-value">14 agents</span>
          <Link to="/conversation" className="stat-link">Start conversation →</Link>
        </div>
      </div>

      <section className="card">
        <h2>Quick actions</h2>
        <div className="action-grid">
          <Link to="/conversation" className="action-card">
            <strong>Ask AI to place an order</strong>
            <span>"I need 50 units of SKU-001"</span>
          </Link>
          <Link to="/orders" className="action-card">
            <strong>Create order manually</strong>
            <span>Select products and quantities</span>
          </Link>
          <Link to="/inventory" className="action-card">
            <strong>Check stock</strong>
            <span>Look up availability by SKU</span>
          </Link>
        </div>
      </section>
    </div>
  );
}
