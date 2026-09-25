## TASK-001 — Backend core, frontend UI, n8n integration hooks

**Status:** IN_PROGRESS
**Priority:** P0
**Owner:** AI agent + TUNZ97
**Type:** backend, frontend, infrastructure
**Dependencies:** Phase 1 scaffolding (done)

### Goal

Deliver a working vertical slice:
`POST /api/messages` → persist → optional n8n webhook → qualify → respond → sales can list leads.

### Acceptance Criteria
- [x] SQLAlchemy models for customers, leads, conversations, messages, activities, follow-ups, notifications
- [x] Alembic configured; initial migration path documented
- [x] Message intake API with idempotency
- [x] Leads list/detail APIs
- [x] Conversation messages API
- [x] Deterministic qualification service
- [x] n8n webhook client (fire-and-forget / configurable)
- [x] Frontend customer chat (orange/yellow modern palette)
- [x] Frontend sales dashboard
- [x] Setup steps for local + n8n

### Related Docs
- docs/PRD.md, docs/API_SPECIFICATION.md, docs/DATABASE_DATA_MODEL_SPECIFICATION.md
- docs/LEAD_QUALIFICATION_SPECIFICATION.md, docs/UI_UX_SPECIFICATION.md, docs/N8N_WORKFLOW_SPECIFICATION.md
