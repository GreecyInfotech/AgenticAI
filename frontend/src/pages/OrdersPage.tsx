import { FormEvent, useEffect, useState } from "react";
import { api, type Order } from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function OrdersPage() {
  const { user } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [sku, setSku] = useState("SKU-001");
  const [qty, setQty] = useState(10);
  const [creating, setCreating] = useState(false);

  function loadOrders() {
    setLoading(true);
    api
      .listOrders()
      .then((res) => setOrders(res.items))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadOrders();
  }, []);

  async function handleCreate(e: FormEvent) {
    e.preventDefault();
    if (!user) return;
    setCreating(true);
    setError("");
    try {
      await api.createOrder(user.subject, [{ sku, quantity: qty }], `order-${Date.now()}`);
      loadOrders();
      setSku("SKU-001");
      setQty(10);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create order");
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h1>Orders</h1>
          <p>Create and manage distributor orders</p>
        </div>
      </header>

      <div className="two-col">
        <section className="card">
          <h2>New order</h2>
          <form onSubmit={handleCreate} className="form-grid">
            <label>
              SKU
              <input value={sku} onChange={(e) => setSku(e.target.value)} required />
            </label>
            <label>
              Quantity
              <input
                type="number"
                min={1}
                value={qty}
                onChange={(e) => setQty(Number(e.target.value))}
                required
              />
            </label>
            <button type="submit" className="btn-primary" disabled={creating}>
              {creating ? "Creating…" : "Place order"}
            </button>
          </form>
          {error && <div className="alert error">{error}</div>}
        </section>

        <section className="card">
          <h2>Order history</h2>
          {loading ? (
            <p>Loading…</p>
          ) : orders.length === 0 ? (
            <p className="muted">No orders yet. Create your first order above.</p>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Order ID</th>
                    <th>Status</th>
                    <th>Total</th>
                    <th>Items</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map((o) => (
                    <tr key={o.order_id}>
                      <td><code>{o.order_id}</code></td>
                      <td><span className="pill">{o.status}</span></td>
                      <td>${o.total.toFixed(2)}</td>
                      <td>{o.items.map((i) => `${i.sku}×${i.quantity}`).join(", ")}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
