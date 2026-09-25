# Local setup & n8n configuration

Step-by-step so frontend, backend, PostgreSQL and n8n work together on your machine.

## 1. Prerequisites

- Docker (for Postgres)
- Python 3.11+
- Node.js 20 LTS
- n8n (`npm install -g n8n` or Docker)

## 2. Clone & env

```bash
git clone https://github.com/TUNZ97/the-real-estate-lead-bot.git
cd the-real-estate-lead-bot
cp .env.example .env
```

Edit `.env` (minimum):

```text
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/real_estate_lead_bot
APP_ENV=development
DEBUG=true
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
N8N_WEBHOOK_URL=http://localhost:5678/webhook
N8N_WEBHOOK_SECRET=dev-secret-change-me
JWT_SECRET=dev-jwt-secret-change-me
```

Also copy env values into `backend/` if you run uvicorn from that folder (or export them in your shell).

## 3. Start PostgreSQL

```bash
docker compose up -d postgres
```

Wait until healthy: `docker compose ps`

## 4. Backend

```bash
cd backend
python -m venv .venv

# Windows PowerShell:
.\env\Scripts\Activate.ps1
# or: .\.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Load env from repo root if needed
# set -a; source ../.env; set +a

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Check:

- http://localhost:8000/health → `{"status":"ok",...}`
- http://localhost:8000/docs → OpenAPI UI

On first start in development, tables are auto-created.

### Quick API test

```bash
curl -X POST http://localhost:8000/api/messages \
  -H "Content-Type: application/json" \
  -d '{"message":"I need a 3-bedroom apartment in Lekki, budget around N80 million","customer_name":"Ada","customer_phone":"08030000000"}'
```

## 5. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

- **Chat** tab: send property enquiries (orange/yellow UI)
- **Sales** tab: see structured leads, filters, status updates

Vite proxies `/api` and `/health` to port 8000.

## 6. n8n (optional but recommended)

### Start n8n

```bash
n8n start
# UI: http://localhost:5678
```

### Create WF-001 Lead Intake webhook

1. New workflow → add **Webhook** node.
2. HTTP Method: **POST**
3. Path: `lead-intake`  
   Full URL becomes: `http://localhost:5678/webhook/lead-intake`
4. (Optional) Add an **IF** or Code node to check header `X-Webhook-Secret` equals `dev-secret-change-me`.
5. Add a **Respond to Webhook** node (200 OK) so the backend does not wait long.
6. Optionally log the body or call an AI node later.
7. **Activate** the workflow.

Backend posts to `{N8N_WEBHOOK_URL}/lead-intake` after every customer message.  
If n8n is down, the chat still works — the webhook error is only logged.

See `n8n/workflows/lead-intake.placeholder.json` for the expected payload shape.

## 7. End-to-end test checklist

1. Postgres up, backend up, frontend up.
2. Chat: “Hi, looking for a 3-bedroom apartment in Lekki, budget N80m”.
3. Bot replies with grounded clarification (no fake listings).
4. Sales page shows a new lead with intent/location/budget/qualification.
5. Change lead status from the dashboard.
6. With n8n active, execution appears for `lead-intake`.

## 8. Troubleshooting

| Issue | Fix |
|-------|-----|
| Backend can't connect to DB | `docker compose up -d postgres`; check `DATABASE_URL` |
| CORS errors | Ensure `CORS_ORIGINS` includes `http://localhost:5173` |
| Frontend 404 on API | Run backend on 8000; Vite proxy is in `vite.config.ts` |
| n8n not receiving | Confirm workflow **Active**, path is `lead-intake`, URL matches `.env` |
| Empty sales list | Send at least one chat message first |

## 9. Architecture reminder

```text
React (chat/sales) → FastAPI → PostgreSQL
                         ↓
                    n8n webhook (optional orchestration / AI)
```

- PostgreSQL = source of truth
- Qualification score = deterministic (backend)
- AI (via n8n later) = interpretation only, validated before trust
