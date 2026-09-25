# Real Estate Lead Bot — PrimeHomes Realty

AI-assisted lead intake and qualification system for PrimeHomes Realty.

It receives natural-language property enquiries, extracts structured requirements, stores the lead, evaluates qualification and urgency deterministically, responds to the customer, alerts the sales team when appropriate, and tracks the lead through its lifecycle.

**Humans stay in control of important sales interactions. AI never invents property facts.**

## Architecture (high level)

```text
Customer → React / Channel → FastAPI → n8n → AI + Notifications
                                ↓
                           PostgreSQL (source of truth)
```

| Component   | Responsibility                                      |
|-------------|-----------------------------------------------------|
| React       | Presentation, chat, sales dashboard                 |
| FastAPI     | API, validation, domain rules, auth, DB access      |
| n8n         | Workflow orchestration, scheduling, notifications   |
| AI          | NLU, extraction, response drafting (validated)      |
| PostgreSQL  | Authoritative application state                     |

## Repository structure

```text
.
├── backend/          # FastAPI application
├── frontend/         # React (Vite + TypeScript) UI
├── n8n/              # Exported n8n workflows
├── docs/             # Approved product & technical specifications
├── tests/            # Cross-cutting and E2E tests
├── .github/          # CI workflows
├── docker-compose.yml
├── .env.example
└── README.md
```

## Documentation (source of truth)

All product and technical decisions live under [`docs/`](./docs/). Start here:

| Document | Purpose |
|----------|---------|
| [PRD.md](./docs/PRD.md) | Product requirements |
| [REAL_ESTATE_LEAD_BOT.md](./docs/REAL_ESTATE_LEAD_BOT.md) | Product overview & principles |
| [SYSTEM_ARCHITECTURE.md](./docs/SYSTEM_ARCHITECTURE.md) | Component boundaries |
| [API_SPECIFICATION.md](./docs/API_SPECIFICATION.md) | HTTP contracts |
| [DATABASE_DATA_MODEL_SPECIFICATION.md](./docs/DATABASE_DATA_MODEL_SPECIFICATION.md) | PostgreSQL model |
| [AI_SPECIFICATION.md](./docs/AI_SPECIFICATION.md) | Safe AI usage |
| [LEAD_QUALIFICATION_SPECIFICATION.md](./docs/LEAD_QUALIFICATION_SPECIFICATION.md) | Deterministic scoring |
| [N8N_WORKFLOW_SPECIFICATION.md](./docs/N8N_WORKFLOW_SPECIFICATION.md) | Workflows |
| [UI_UX_SPECIFICATION.md](./docs/UI_UX_SPECIFICATION.md) | Customer & sales UX |
| [IMPLEMENTATION.md](./docs/IMPLEMENTATION.md) | Phased delivery plan |
| [DEVELOPMENT_SETUP.md](./docs/DEVELOPMENT_SETUP.md) | Local setup |
| [TESTING_SPECIFICATION.md](./docs/TESTING_SPECIFICATION.md) | Test strategy |
| [DEPLOYMENT_SPECIFICATION.md](./docs/DEPLOYMENT_SPECIFICATION.md) | Environments & release |
| [TASK.md](./docs/TASK.md) | Task system for implementation |

## Quick start (local)

### Prerequisites

- Python 3.11+
- Node.js LTS
- PostgreSQL 15+
- n8n (local or Docker)
- Git

### 1. Clone & environment

```bash
git clone https://github.com/TUNZ97/the-real-estate-lead-bot.git
cd the-real-estate-lead-bot
cp .env.example .env
# Edit .env with your local values
```

### 2. Database (Docker)

```bash
docker compose up -d postgres
```

### 3. Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 5. n8n

```bash
n8n start
# Import workflows from n8n/workflows/ when available
```

## Operating principles

- Never fabricate property availability, pricing or facts.
- Validate all AI structured output before persistence.
- Qualification and urgency are **deterministic** (not AI judgment).
- PostgreSQL is the single source of truth.
- Important automated actions are auditable and preferably idempotent.
- Human handoff is always available.

## Implementation phases

See [docs/IMPLEMENTATION.md](./docs/IMPLEMENTATION.md). Current focus: **Phase 1 — Project foundation**.

## License

MIT — see [LICENSE](./LICENSE).
