import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

function CustomerChat() {
  return (
    <div className="page">
      <h1>PrimeHomes</h1>
      <p className="subtitle">Property enquiry chat (Phase 7)</p>
      <div className="chat-shell">
        <div className="messages">
          <p className="muted">
            Customer chat UI will connect to <code>POST /api/messages</code>.
          </p>
        </div>
        <form
          className="composer"
          onSubmit={(e) => {
            e.preventDefault();
          }}
        >
          <input
            type="text"
            placeholder="Describe the property you need…"
            disabled
            aria-label="Message"
          />
          <button type="submit" disabled>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

function SalesDashboard() {
  return (
    <div className="page">
      <h1>Sales dashboard</h1>
      <p className="subtitle">Lead list & filters (Phase 8)</p>
      <p className="muted">Placeholder — will list leads from GET /api/leads.</p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <nav className="nav">
        <Link to="/">Chat</Link>
        <Link to="/sales">Sales</Link>
      </nav>
      <Routes>
        <Route path="/" element={<CustomerChat />} />
        <Route path="/sales" element={<SalesDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
