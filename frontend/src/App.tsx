import { FormEvent, useEffect, useRef, useState } from "react";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import {
  ChatMessage,
  Lead,
  getConversationMessages,
  listLeads,
  sendMessage,
  updateLeadStatus,
} from "./api/client";

type UiMessage = {
  id: string;
  role: "customer" | "bot" | "system";
  content: string;
};

const STORAGE_KEY = "relb_conversation_id";

function CustomerChat() {
  const [messages, setMessages] = useState<UiMessage[]>([
    {
      id: "welcome",
      role: "bot",
      content:
        "Hi! I'm the PrimeHomes assistant. Tell me what property you're looking for — area, budget, bedrooms — and I'll help get you started.",
    },
  ]);
  const [text, setText] = useState("");
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(
    () => localStorage.getItem(STORAGE_KEY)
  );
  const [leadId, setLeadId] = useState<string | null>(null);
  const [qualification, setQualification] = useState<string | null>(null);
  const [urgency, setUrgency] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (!conversationId) return;
    getConversationMessages(conversationId)
      .then((rows: ChatMessage[]) => {
        if (!rows.length) return;
        setMessages(
          rows.map((m) => ({
            id: m.id,
            role:
              m.sender_type === "CUSTOMER"
                ? "customer"
                : m.sender_type === "BOT"
                  ? "bot"
                  : "system",
            content: m.content,
          }))
        );
      })
      .catch(() => {
        /* keep local state */
      });
  }, [conversationId]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    setError(null);
    setLoading(true);
    const optimisticId = `local-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      { id: optimisticId, role: "customer", content: trimmed },
    ]);
    setText("");

    try {
      const res = await sendMessage({
        message: trimmed,
        conversation_id: conversationId,
        customer_name: name || undefined,
        customer_phone: phone || undefined,
      });
      setConversationId(res.conversation_id);
      localStorage.setItem(STORAGE_KEY, res.conversation_id);
      if (res.lead_id) setLeadId(res.lead_id);
      if (res.qualification_level) setQualification(res.qualification_level);
      if (res.urgency) setUrgency(res.urgency);

      setMessages((prev) => [
        ...prev,
        {
          id: res.message_id + "-bot",
          role: "bot",
          content: res.response,
        },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
      setMessages((prev) => prev.filter((m) => m.id !== optimisticId));
      setText(trimmed);
    } finally {
      setLoading(false);
    }
  }

  function resetChat() {
    localStorage.removeItem(STORAGE_KEY);
    setConversationId(null);
    setLeadId(null);
    setQualification(null);
    setUrgency(null);
    setMessages([
      {
        id: "welcome",
        role: "bot",
        content:
          "Hi! I'm the PrimeHomes assistant. Tell me what property you're looking for — area, budget, bedrooms — and I'll help get you started.",
      },
    ]);
  }

  return (
    <div className="page">
      <h1>PrimeHomes Chat</h1>
      <p className="subtitle">
        Tell us what you need — we'll structure it for our sales team.
      </p>

      <div className="meta-bar">
        {conversationId && (
          <span className="chip">Conversation active</span>
        )}
        {leadId && <span className="chip">Lead linked</span>}
        {qualification && (
          <span className={`chip ${qualification.toLowerCase()}`}>
            Qual: {qualification}
          </span>
        )}
        {urgency && (
          <span className={`chip ${urgency.toLowerCase()}`}>
            Urgency: {urgency}
          </span>
        )}
        <button type="button" className="btn btn-ghost" onClick={resetChat}>
          New chat
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="contact-row">
        <div className="field">
          <label htmlFor="name">Your name (optional)</label>
          <input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Ada Okafor"
          />
        </div>
        <div className="field">
          <label htmlFor="phone">Phone (optional)</label>
          <input
            id="phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="0803…"
          />
        </div>
      </div>

      <div className="chat-shell">
        <div className="messages">
          {messages.map((m) => (
            <div key={m.id} className={`bubble ${m.role}`}>
              {m.content}
            </div>
          ))}
          {loading && <div className="typing">PrimeHomes is typing…</div>}
          <div ref={bottomRef} />
        </div>
        <form className="composer" onSubmit={onSubmit}>
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="e.g. 3-bedroom apartment in Lekki, budget around N80m"
            aria-label="Message"
            disabled={loading}
          />
          <button className="btn" type="submit" disabled={loading || !text.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

function SalesDashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [total, setTotal] = useState(0);
  const [status, setStatus] = useState("");
  const [qualification, setQualification] = useState("");
  const [urgency, setUrgency] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const res = await listLeads({
        limit: 50,
        status: status || undefined,
        qualification: qualification || undefined,
        urgency: urgency || undefined,
      });
      setLeads(res.items);
      setTotal(res.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load leads");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [status, qualification, urgency]);

  async function onStatus(id: string, next: string) {
    try {
      const updated = await updateLeadStatus(id, next);
      setLeads((prev) => prev.map((l) => (l.id === id ? updated : l)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Status update failed");
    }
  }

  function formatBudget(l: Lead) {
    if (!l.budget_min && !l.budget_max) return "—";
    const cur = l.currency || "NGN";
    if (l.budget_min && l.budget_max)
      return `${cur} ${l.budget_min} – ${l.budget_max}`;
    if (l.budget_max) return `up to ${cur} ${l.budget_max}`;
    return `from ${cur} ${l.budget_min}`;
  }

  return (
    <div className="page page-wide">
      <h1>Sales dashboard</h1>
      <p className="subtitle">
        {total} lead{total === 1 ? "" : "s"} · structured from customer chat
      </p>

      <div className="filters">
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All statuses</option>
          <option value="NEW">NEW</option>
          <option value="CONTACTED">CONTACTED</option>
          <option value="QUALIFIED">QUALIFIED</option>
          <option value="FOLLOW_UP">FOLLOW_UP</option>
          <option value="CONVERTED">CONVERTED</option>
          <option value="LOST">LOST</option>
        </select>
        <select
          value={qualification}
          onChange={(e) => setQualification(e.target.value)}
        >
          <option value="">All qualification</option>
          <option value="HIGH">HIGH</option>
          <option value="MEDIUM">MEDIUM</option>
          <option value="LOW">LOW</option>
          <option value="UNKNOWN">UNKNOWN</option>
        </select>
        <select value={urgency} onChange={(e) => setUrgency(e.target.value)}>
          <option value="">All urgency</option>
          <option value="HIGH">HIGH</option>
          <option value="MEDIUM">MEDIUM</option>
          <option value="LOW">LOW</option>
        </select>
        <button type="button" className="btn" onClick={load}>
          Refresh
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {loading ? (
        <p className="muted">Loading leads…</p>
      ) : leads.length === 0 ? (
        <div className="empty card">
          No leads yet. Send a message from the customer chat to create one.
        </div>
      ) : (
        <div className="lead-grid">
          {leads.map((l) => (
            <article key={l.id} className="card lead-card">
              <h3>{l.customer_name || "Anonymous prospect"}</h3>
              <p className="muted">
                {l.customer_phone || l.customer_email || "No contact yet"}
              </p>
              <div className="lead-meta">
                <span className="chip">{l.intent}</span>
                <span className="chip">{l.property_type}</span>
                <span className={`chip ${l.qualification_level.toLowerCase()}`}>
                  {l.qualification_level}
                  {l.qualification_score != null
                    ? ` · ${l.qualification_score}`
                    : ""}
                </span>
                <span className={`chip ${l.urgency.toLowerCase()}`}>
                  {l.urgency}
                </span>
                <span className="chip">{l.status}</span>
              </div>
              <p>
                <strong>Location:</strong> {l.location_text || "—"}
                {l.bedrooms != null ? ` · ${l.bedrooms} bed` : ""}
              </p>
              <p>
                <strong>Budget:</strong> {formatBudget(l)}
              </p>
              <p className="muted">
                {new Date(l.created_at).toLocaleString()}
              </p>
              <div className="filters" style={{ marginTop: "0.75rem" }}>
                <select
                  defaultValue=""
                  onChange={(e) => {
                    if (e.target.value) onStatus(l.id, e.target.value);
                    e.target.value = "";
                  }}
                >
                  <option value="">Update status…</option>
                  <option value="CONTACTED">CONTACTED</option>
                  <option value="QUALIFIED">QUALIFIED</option>
                  <option value="FOLLOW_UP">FOLLOW_UP</option>
                  <option value="CONVERTED">CONVERTED</option>
                  <option value="LOST">LOST</option>
                </select>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <nav className="nav">
        <div className="nav-brand">PrimeHomes</div>
        <div className="nav-links">
          <Link to="/">Chat</Link>
          <Link to="/sales">Sales</Link>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<CustomerChat />} />
        <Route path="/sales" element={<SalesDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
