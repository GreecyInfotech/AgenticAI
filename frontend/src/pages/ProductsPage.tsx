import { useEffect, useState } from "react";
import { api, type Product } from "../api/client";

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .listProducts()
      .then((res) => setProducts(res.items))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h1>Products</h1>
          <p>Browse the distributor product catalog</p>
        </div>
      </header>

      {error && <div className="alert error">{error}</div>}

      {loading ? (
        <p>Loading products…</p>
      ) : (
        <div className="product-grid">
          {products.map((p) => (
            <article key={p.sku} className="product-card card">
              <span className="product-sku">{p.sku}</span>
              <h3>{p.name}</h3>
              {p.category && <span className="pill">{p.category}</span>}
              <div className="product-price">${p.price.toFixed(2)}</div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
