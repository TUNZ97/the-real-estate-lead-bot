# Backend — FastAPI

Authoritative API, domain logic, validation, auth and database access for the Real Estate Lead Bot.

**Local development database: MySQL** (no Docker required).

See [docs/LOCAL_SETUP_AND_N8N.md](../docs/LOCAL_SETUP_AND_N8N.md).

## Layout

```text
backend/
├── app/
│   ├── api/v1/          # HTTP routes
│   ├── core/            # config, security, errors
│   ├── db/              # engine & session
│   ├── models/          # SQLAlchemy models
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── alembic/
├── requirements.txt
└── README.md
```

## Run locally

1. Create MySQL database `real_estate_lead_bot`.
2. Set in repo-root `.env`:

```text
DATABASE_URL=mysql+aiomysql://root:YOUR_PASSWORD@127.0.0.1:3306/real_estate_lead_bot
```

3. Install and start:

```bash
cd backend
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: http://localhost:8000/health  
- OpenAPI: http://localhost:8000/docs  

Tables are auto-created on startup when `APP_ENV=development`.
