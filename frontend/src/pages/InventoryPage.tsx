import { FormEvent, useState } from "react";
import { api, type InventoryItem } from "../api/client";

export default function InventoryPage() {
  const [sku, setSku] = useState("SKU-001");
  const [item, setItem] = useState<InventoryItem | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLookup(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setItem(null);
    try {
      const res = await api.getInventory(sku.trim());
      setItem(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Lookup failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h1>Inventory</h1>
          <p>Real-time stock availability by SKU</p>
        </div>
      </header>

      <section className="card" style={{ maxWidth: 480 }}>
        <form onSubmit={handleLookup} className="form-grid">
          <label>
            SKU
            <input value={sku} onChange={(e) => setSku(e.target.value)} placeholder="SKU-001" required />
          </label>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Checking…" : "Check stock"}
          </button>
        </form>
        {error && <div className="alert error">{error}</div>}
        {item && (
          <div className="inventory-result">
            <div className="inventory-qty">{item.available}</div>
            <div>
              <strong>{item.sku}</strong>
              <p className="muted">Warehouse: {item.warehouse}</p>
            </div>
            <span className={`status-badge ${item.available > 0 ? "up" : "down"}`}>
              {item.available > 0 ? "In stock" : "Out of stock"}
            </span>
          </div>
        )}
      </section>

      <div className="suggestions">
        {["SKU-001", "SKU-002", "SKU-12345"].map((s) => (
          <button key={s} type="button" className="chip" onClick={() => setSku(s)}>
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
