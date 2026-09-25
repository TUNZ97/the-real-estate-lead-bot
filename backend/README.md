# Backend — FastAPI

Authoritative API, domain logic, validation, auth and database access for the Real Estate Lead Bot.

See [docs/SYSTEM_ARCHITECTURE.md](../docs/SYSTEM_ARCHITECTURE.md) and [docs/API_SPECIFICATION.md](../docs/API_SPECIFICATION.md).

## Layout

```text
backend/
├── app/
│   ├── api/v1/          # HTTP routes
│   ├── core/            # config, security, errors
│   ├── db/              # engine & session (Phase 2)
│   ├── models/          # SQLAlchemy models (Phase 2)
│   ├── repositories/    # data access (Phase 3)
│   ├── schemas/         # Pydantic schemas (Phase 3)
│   ├── services/        # domain services (Phase 3+)
│   └── main.py          # FastAPI entrypoint
├── alembic/             # migrations (Phase 2)
├── requirements.txt
└── README.md
```

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Ensure PostgreSQL is running and DATABASE_URL is set (see root .env.example)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: http://localhost:8000/health
- OpenAPI docs (dev): http://localhost:8000/docs

## Implementation order

Config → database → models → repositories → services → API schemas/routes → auth → integrations → tests.
