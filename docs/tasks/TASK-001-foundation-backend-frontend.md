## TASK-001 — Backend core, frontend UI, n8n integration hooks

**Status:** DONE
**Priority:** P0
**Owner:** AI agent + TUNZ97
**Type:** backend, frontend, infrastructure
**Dependencies:** Phase 1 scaffolding (done)

### Goal

Deliver a working vertical slice:
`POST /api/messages` → persist → optional n8n webhook → qualify → respond → sales can list leads.

### Acceptance Criteria
- [x] SQLAlchemy models for customers, leads, conversations, messages, activities, follow-ups, notifications
- [x] Tables auto-created in development on startup
- [x] Message intake API with idempotency
- [x] Leads list/detail/patch/status/qualify APIs
- [x] Conversation messages API
- [x] Deterministic qualification service
- [x] Lightweight extraction heuristics (MVP without AI)
- [x] n8n webhook client (fire-and-forget)
- [x] Frontend customer chat (orange/yellow modern palette)
- [x] Frontend sales dashboard with filters + status
- [x] Setup guide: docs/LOCAL_SETUP_AND_N8N.md

### How to run

See [docs/LOCAL_SETUP_AND_N8N.md](../LOCAL_SETUP_AND_N8N.md).

### Related Docs
- docs/PRD.md, docs/API_SPECIFICATION.md, docs/DATABASE_DATA_MODEL_SPECIFICATION.md
- docs/LEAD_QUALIFICATION_SPECIFICATION.md, docs/UI_UX_SPECIFICATION.md, docs/N8N_WORKFLOW_SPECIFICATION.md
