import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "/api";
const B2C_AGENTS = ["support", "order"];

interface Agent { id: string; name: string; description: string; }

export default function App() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selected, setSelected] = useState("support");
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  useEffect(() => {
    fetch(`${API}/agents`).then((r) => r.json()).then((list: Agent[]) =>
      setAgents(list.filter((a) => B2C_AGENTS.includes(a.id)))
    );
  }, []);

  const run = async () => {
    const res = await fetch(`${API}/agents/${selected}/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, portal: "b2c" }),
    });
    const data = await res.json();
    setAnswer(data.answer || JSON.stringify(data));
  };

  return (
    <div style={{ maxWidth: 720, margin: "0 auto", padding: 24 }}>
      <h1>Customer Assistant</h1>
      <p>Get help with orders and support</p>
      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        {agents.map((a) => (
          <button key={a.id} onClick={() => setSelected(a.id)}
            style={{ padding: "8px 16px", background: selected === a.id ? "#7c3aed" : "#ede9fe", color: selected === a.id ? "#fff" : "#1e1b4b", border: "none", borderRadius: 999 }}>
            {a.name.replace("-agent", "")}
          </button>
        ))}
      </div>
      <textarea value={query} onChange={(e) => setQuery(e.target.value)} rows={3}
        style={{ width: "100%", padding: 12, borderRadius: 12, border: "1px solid #c4b5fd" }}
        placeholder="How can we help you today?" />
      <button onClick={run} style={{ marginTop: 12, padding: "10px 24px", background: "#7c3aed", color: "#fff", border: "none", borderRadius: 999 }}>
        Ask
      </button>
      {answer && <div style={{ marginTop: 20, padding: 16, background: "#fff", borderRadius: 12, border: "1px solid #ddd6fe" }}>{answer}</div>}
    </div>
  );
}
