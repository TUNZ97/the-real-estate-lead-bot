# Local setup (MySQL + npm — no Docker)

Development stack on your PC:

- **MySQL** (already installed on your machine)
- **Python** backend (FastAPI)
- **Node/npm** frontend (Vite) and optional **n8n**

Docker is **not** required for local development.

## 1. Prerequisites

- MySQL Server running locally (default port **3306**)
- Python 3.11+
- Node.js LTS + npm
- n8n via npm (optional): `npm install -g n8n`

## 2. Create the MySQL database

Open MySQL (Workbench, CLI, or phpMyAdmin) and run:

```sql
CREATE DATABASE IF NOT EXISTS real_estate_lead_bot
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Use a user that can access this database (often `root` on local Windows installs).

## 3. Clone & configure env

```bash
git clone https://github.com/TUNZ97/the-real-estate-lead-bot.git
cd the-real-estate-lead-bot
git pull origin main
cp .env.example .env
```

Edit `.env` — **set your real MySQL password**:

```text
DATABASE_URL=mysql+aiomysql://root:YOUR_MYSQL_PASSWORD@127.0.0.1:3306/real_estate_lead_bot
APP_ENV=development
DEBUG=true
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
N8N_WEBHOOK_URL=http://localhost:5678/webhook
N8N_WEBHOOK_SECRET=dev-secret-change-me
JWT_SECRET=dev-jwt-secret-change-me
```

URL-encode special characters in the password if needed (e.g. `@` → `%40`).

## 4. Backend

```bash
cd backend
python -m venv .venv

# Windows PowerShell:
.\env\Scripts\Activate.ps1
# if folder is .venv:
.\\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

On first start in development, tables are created automatically in MySQL.

Check:

- http://localhost:8000/health
- http://localhost:8000/docs

### API smoke test

```bash
curl -X POST http://localhost:8000/api/messages ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"3-bedroom apartment in Lekki, budget N80m\",\"customer_name\":\"Ada\"}"
```

## 5. Frontend (npm)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

- **Chat** — orange/yellow customer UI  
- **Sales** — lead list, filters, status updates  

Vite proxies `/api` → `http://localhost:8000`.

## 6. n8n (npm, optional)

```bash
n8n start
```

1. Open http://localhost:5678  
2. New workflow → **Webhook** node  
3. Method **POST**, path **`lead-intake`**  
4. Activate the workflow  

Backend calls: `http://localhost:5678/webhook/lead-intake`  
If n8n is stopped, chat still works (webhook is best-effort).

## 7. End-to-end checklist

1. MySQL running; database `real_estate_lead_bot` exists  
2. Backend starts without DB connection errors  
3. Chat message creates a lead  
4. Sales page shows the lead  
5. (Optional) n8n shows a `lead-intake` execution  

## 8. Troubleshooting

| Issue | Fix |
|-------|-----|
| `Access denied for user` | Fix user/password in `DATABASE_URL` |
| `Unknown database` | Run the `CREATE DATABASE` statement above |
| `Can't connect to MySQL` | Start MySQL service; confirm port 3306 |
| Password has `@` `#` etc. | URL-encode it in `DATABASE_URL` |
| CORS errors | Keep `CORS_ORIGINS` including `http://localhost:5173` |
| Tables missing | Restart backend with `APP_ENV=development` (auto `create_all`) |

## 9. Architecture (local)

```text
React (npm) → FastAPI → MySQL (local)
                   ↓
              n8n (npm, optional)
```

Deployment later may use Docker/Postgres; local development is intentionally MySQL + npm only.
