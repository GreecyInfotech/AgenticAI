import { FormEvent, useRef, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

interface Message {
  role: "user" | "assistant";
  content: string;
  agent?: string | null;
}

export default function ConversationPage() {
  const { user } = useAuth();
  const sessionId = useRef(`sess-${Date.now()}`);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hello! I'm your AI ordering assistant. Ask about inventory, pricing, orders, or shipments.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!input.trim() || !user || loading) return;

    const userMsg = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      const res = await api.converse(sessionId.current, user.subject, userMsg);
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: res.reply || "No response generated.",
          agent: res.target_agent,
        },
      ]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: err instanceof Error ? err.message : "Request failed" },
      ]);
    } finally {
      setLoading(false);
      setTimeout(() => bottomRef.current?.scrollIntoView({ behavior: "smooth" }), 50);
    }
  }

  return (
    <div className="page conversation-page">
      <header className="page-header">
        <div>
          <h1>AI Assistant</h1>
          <p>LangGraph orchestrator routes to 14 specialist agents</p>
        </div>
      </header>

      <div className="chat-container card">
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-bubble ${msg.role}`}>
              {msg.agent && <span className="agent-tag">{msg.agent}</span>}
              <p>{msg.content}</p>
            </div>
          ))}
          {loading && (
            <div className="chat-bubble assistant">
              <p className="typing">Thinking…</p>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <form className="chat-input" onSubmit={handleSubmit}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g. Check stock for SKU-001 or place an order for 10 widgets"
            disabled={loading}
          />
          <button type="submit" className="btn-primary" disabled={loading || !input.trim()}>
            Send
          </button>
        </form>
      </div>

      <div className="suggestions">
        {[
          "What is the price for SKU-001?",
          "Check inventory for SKU-12345",
          "I want to place an order for 20 units of SKU-001",
          "Track my recent shipment",
        ].map((s) => (
          <button key={s} type="button" className="chip" onClick={() => setInput(s)}>
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
