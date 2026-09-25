# Development Setup

Local development uses **MySQL on your PC** and **npm** for the frontend / n8n. **Docker is not required** for day-to-day development.

For the full step-by-step runbook see [LOCAL_SETUP_AND_N8N.md](./LOCAL_SETUP_AND_N8N.md).

## 1. Prerequisites

- Windows 10/11 or compatible development OS
- Git
- Python 3.11+
- Node.js LTS + npm
- **MySQL Server** (local install, port 3306)
- n8n via npm (optional): `npm install -g n8n`
- ngrok only if a public webhook URL is needed
- VS Code / Cursor or equivalent editor

## 2. Repository setup

```powershell
git clone https://github.com/TUNZ97/the-real-estate-lead-bot.git
cd the-real-estate-lead-bot
cp .env.example .env
```

Edit `.env` and set:

```text
DATABASE_URL=mysql+aiomysql://root:YOUR_MYSQL_PASSWORD@127.0.0.1:3306/real_estate_lead_bot
```

## 3. MySQL database

```sql
CREATE DATABASE IF NOT EXISTS real_estate_lead_bot
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

No Docker database container is used in local development.

## 4. Backend

```powershell
cd backend
python -m venv .venv
.\env\Scripts\Activate.ps1
# or: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In `APP_ENV=development`, tables are created automatically on startup.

## 5. Frontend

```powershell
cd frontend
npm install
npm run dev
```

## 6. n8n

```powershell
n8n start
```

Use a local n8n instance. Do not expose it publicly without authentication.

## 7. Environment variables

Examples:

```text
DATABASE_URL=mysql+aiomysql://root:password@127.0.0.1:3306/real_estate_lead_bot
AI_API_KEY=
AI_MODEL=
N8N_BASE_URL=http://localhost:5678
N8N_WEBHOOK_SECRET=
JWT_SECRET=
FRONTEND_URL=http://localhost:5173
```

Never commit real credentials.

## 8. Git workflow

Use focused branches and commits. Review changes before merging.

## 9. Debugging

- API: FastAPI logs and `/docs`
- Database: MySQL connection string, user permissions, database exists
- n8n: execution input/output and failed nodes
- Frontend: browser network tab and API error payloads

## 10. AI coding agent workflow

Before coding, read the PRD, architecture, API, database, relevant feature specification and task. Implement the smallest coherent change, run relevant tests, update docs when contracts change, and avoid inventing architecture.
