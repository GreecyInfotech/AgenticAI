import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "/api";
const B2B_AGENTS = ["backlog", "architecture", "sales", "order"];

interface Agent { id: string; name: string; description: string; }

export default function App() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selected, setSelected] = useState("backlog");
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [healthy, setHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    fetch(`${API}/health`).then((r) => setHealthy(r.ok)).catch(() => setHealthy(false));
    fetch(`${API}/agents`).then((r) => r.json()).then((list: Agent[]) =>
      setAgents(list.filter((a) => B2B_AGENTS.includes(a.id)))
    );
  }, []);

  const run = async () => {
    const res = await fetch(`${API}/agents/${selected}/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, portal: "b2b" }),
    });
    const data = await res.json();
    setAnswer(data.answer || JSON.stringify(data));
  };

  return (
    <div style={{ maxWidth: 960, margin: "0 auto", padding: 24 }}>
      <header style={{ display: "flex", justifyContent: "space-between", marginBottom: 24 }}>
        <div>
          <h1>EAAP B2B Portal</h1>
          <p>Enterprise agentic workflows for business users</p>
        </div>
        <span style={{ color: healthy ? "#4ade80" : "#f87171" }}>
          {healthy === null ? "..." : healthy ? "API Online" : "API Offline"}
        </span>
      </header>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 16 }}>
        {agents.map((a) => (
          <button key={a.id} onClick={() => setSelected(a.id)}
            style={{ padding: "8px 12px", background: selected === a.id ? "#2563eb" : "#1e293b", color: "#fff", border: "none", borderRadius: 8 }}>
            {a.name}
          </button>
        ))}
      </div>
      <textarea value={query} onChange={(e) => setQuery(e.target.value)} rows={4}
        style={{ width: "100%", padding: 12, borderRadius: 8, background: "#1e293b", color: "#fff", border: "1px solid #334155" }}
        placeholder="Ask a B2B agent..." />
      <button onClick={run} style={{ marginTop: 12, padding: "10px 20px", background: "#2563eb", color: "#fff", border: "none", borderRadius: 8 }}>
        Run Agent
      </button>
      {answer && <pre style={{ marginTop: 20, padding: 16, background: "#1e293b", borderRadius: 8, whiteSpace: "pre-wrap" }}>{answer}</pre>}
    </div>
  );
}
