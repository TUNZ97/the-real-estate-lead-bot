# Real Estate Lead Bot — PrimeHomes Realty

AI-assisted lead intake and qualification system for PrimeHomes Realty.

It receives natural-language property enquiries, extracts structured requirements, stores the lead, evaluates qualification and urgency deterministically, responds to the customer, alerts the sales team when appropriate, and tracks the lead through its lifecycle.

**Humans stay in control of important sales interactions. AI never invents property facts.**

## Architecture (high level)

```text
Customer → React / Channel → FastAPI → n8n → AI + Notifications
                                ↓
                           MySQL (local development)
```

| Component | Responsibility |
|-----------|----------------|
| React | Presentation, chat, sales dashboard |
| FastAPI | API, validation, domain rules, auth, DB access |
| n8n | Workflow orchestration, scheduling, notifications |
| AI | NLU, extraction, response drafting (validated) |
| MySQL | Application state for local development |

> Deployment later may use Docker/other databases; **local development uses MySQL on your PC (no Docker required).**

## Repository structure

```text
.
├── backend/          # FastAPI application
├── frontend/         # React (Vite + TypeScript) UI
├── n8n/              # Exported n8n workflows
├── docs/             # Approved product & technical specifications
├── tests/
├── .env.example
└── README.md
```

## Documentation

All product and technical decisions live under [`docs/`](./docs/).  
**Local runbook (MySQL + npm):** [docs/LOCAL_SETUP_AND_N8N.md](./docs/LOCAL_SETUP_AND_N8N.md)

## Quick start (local — no Docker)

### Prerequisites

- Python 3.11+
- Node.js LTS + npm
- **MySQL** running on your PC (port 3306)
- n8n via npm (optional): `npm install -g n8n`
- Git

### 1. Clone & environment

```bash
git clone https://github.com/TUNZ97/the-real-estate-lead-bot.git
cd the-real-estate-lead-bot
cp .env.example .env
```

Set your MySQL password in `.env`:

```text
DATABASE_URL=mysql+aiomysql://root:YOUR_MYSQL_PASSWORD@127.0.0.1:3306/real_estate_lead_bot
```

### 2. Create MySQL database

```sql
CREATE DATABASE IF NOT EXISTS real_estate_lead_bot
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Backend

```bash
cd backend
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Tables are auto-created on first start in development.

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

### 5. n8n (optional)

```bash
n8n start
```

Create a **POST** webhook with path `lead-intake` and activate it.

## Operating principles

- Never fabricate property availability, pricing or facts.
- Validate all AI structured output before persistence.
- Qualification and urgency are **deterministic** (not AI judgment).
- The database is the authoritative application state.
- Important automated actions are auditable and preferably idempotent.
- Human handoff is always available.

## Implementation phases

See [docs/IMPLEMENTATION.md](./docs/IMPLEMENTATION.md).

## License

MIT — see [LICENSE](./LICENSE).
