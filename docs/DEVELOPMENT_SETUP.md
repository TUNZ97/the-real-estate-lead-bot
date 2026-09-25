# Development Setup

## 1. Prerequisites

- Windows 10/11 or compatible development OS
- Git
- Python 3.x according to the project version policy
- Node.js LTS
- npm
- PostgreSQL
- n8n
- ngrok for local public webhooks when required
- VS Code/Cursor or equivalent editor

## 2. Repository setup

```powershell
git clone <repository-url>
cd <repository>
```

## 3. Backend

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the FastAPI application using the project's configured command, typically through Uvicorn.

## 4. Database

Create a local PostgreSQL database, configure `DATABASE_URL`, then run Alembic migrations.

```powershell
alembic upgrade head
```

## 5. Frontend

```powershell
cd frontend
npm install
npm run dev
```

## 6. n8n

If installed with npm:

```powershell
n8n start
```

Use a local n8n instance for development. Do not expose it publicly without authentication/security controls.

## 7. ngrok

Use ngrok only when a third-party webhook needs a public HTTPS callback during development. Keep the generated URL in environment configuration rather than hard-coding it.

## 8. Environment variables

Examples:

```text
DATABASE_URL=
AI_API_KEY=
AI_MODEL=
N8N_BASE_URL=
N8N_WEBHOOK_SECRET=
JWT_SECRET=
FRONTEND_URL=
```

Never commit real credentials.

## 9. Git workflow

Use focused branches and commits. Review changes before merging. Keep generated files and line-ending changes intentional. A Windows warning about LF changing to CRLF is a line-ending normalization issue, not automatically a code error.

## 10. Debugging

- API: inspect FastAPI logs and request IDs.
- Database: inspect migration/version state and query errors.
- n8n: inspect execution input/output and failed nodes.
- AI: log schema validation errors, model/prompt versions and safe metadata.
- Frontend: inspect browser network requests and API error payloads.

## 11. AI coding agent workflow

Before coding, read the PRD, architecture, API, database, relevant feature specification and task. Implement the smallest coherent change, run relevant tests, update docs when contracts change, and avoid inventing architecture.
