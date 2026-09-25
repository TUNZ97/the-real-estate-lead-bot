# Implementation

## 1. Objective

Build the MVP in dependency order while preserving the architecture and contracts defined by the other specifications.

## 2. Phases

### Phase 1 — Project foundation
Repository structure, environment configuration, backend/frontend shells, CI basics.

### Phase 2 — Database
PostgreSQL schema, SQLAlchemy models, Alembic migrations, seed/test data.

### Phase 3 — Backend core
FastAPI app, configuration, auth, repositories, services, lead/conversation/message APIs.

### Phase 4 — AI extraction
Provider adapter, prompts, structured schema, validation, confidence handling and tests.

### Phase 5 — n8n
Implement intake, qualification, response, notification, handoff, follow-up and error workflows.

### Phase 6 — Qualification
Implement deterministic score, urgency, missing information and recalculation.

### Phase 7 — Customer conversation
Connect UI/channel to message API and response flow.

### Phase 8 — Sales UI
Dashboard, lead detail, conversation, status and follow-up controls.

### Phase 9 — Notifications/follow-up
Notification delivery, scheduled jobs and activity recording.

### Phase 10 — Testing
Unit, integration, workflow, AI evaluation, E2E and security tests.

### Phase 11 — Deployment
Staging, migrations, secrets, monitoring, production rollout and rollback verification.

### Phase 12 — MVP validation
Run representative real-world scenarios and fix gaps before expansion.

## 3. Suggested repository

```text
backend/
frontend/
n8n/
docs/
tests/
```

## 4. Backend implementation order

Config → database → models → repositories → services → API schemas/routes → auth → integrations → tests.

## 5. First vertical slice

Implement one complete flow before building every feature independently:

`POST message → persist → extract → validate → create/update lead → qualify → respond → record activity`.

This creates an end-to-end foundation for later workflow automation.

## 6. n8n implementation order

WF-001 Intake → WF-002 Qualification → WF-003 Response → WF-004 Notification → WF-005 Handoff → WF-006 Follow-up → remaining support workflows.

## 7. Frontend implementation order

Customer chat → API integration → lead dashboard → lead detail → status/actions → follow-up → error/loading states → responsive/accessibility refinement.

## 8. What not to build first

Do not start with microservices, Kubernetes, complex recommendation engines, elaborate analytics or autonomous negotiation. Stabilize the core lead loop first.

## 9. Definition of Done

Every implementation increment must satisfy its task acceptance criteria, tests, architecture boundaries, security requirements and documentation obligations.
