# System Architecture

## 1. Goals

Provide a simple, testable architecture where each component has a clear responsibility and where AI automation does not compromise application correctness.

## 2. Architecture

```text
┌───────────────┐
│ Customer / UI │
└───────┬───────┘
        ↓
┌──────────────────┐
│ React Frontend   │
└────────┬─────────┘
         ↓ HTTPS/JSON
┌──────────────────┐
│ FastAPI Backend  │
│ API + Domain     │
└───────┬──────────┘
        ├──────────────→ PostgreSQL
        └──────────────→ n8n
                           ├→ AI provider
                           ├→ Notifications
                           └→ Integrations
```

## 3. Component boundaries

### React
Presentation, forms, chat, dashboard, status display and user interaction. It must not contain authoritative qualification or security decisions.

### FastAPI
Authentication/authorization, request validation, domain rules, database access, lifecycle transitions, idempotency and stable API contracts.

### n8n
Workflow orchestration, event routing, external integrations, scheduled jobs and notification flows.

### AI
Natural-language interpretation and generation. AI output is untrusted until validated.

### PostgreSQL
Source of truth for customers, leads, conversations, messages, activities, follow-ups and notifications.

## 4. Core flows

### Lead intake
1. Customer sends message.
2. Backend validates and records it.
3. Backend starts/updates conversation.
4. n8n processes the event.
5. AI extracts structured information.
6. Backend validates the result.
7. Lead is created/updated.
8. Qualification is recalculated.
9. Customer response is generated and delivered.
10. Sales notification is triggered when rules require it.

### Follow-up
Scheduled n8n workflow finds due follow-ups → validates lead state → sends or requests a follow-up → records activity → updates follow-up state.

## 5. Data authority

PostgreSQL is authoritative. Google Sheets, notification systems and AI context are derived/operational representations.

## 6. Reliability

- Idempotency keys/external message IDs prevent duplicate processing.
- Retry transient integration failures.
- Do not retry non-idempotent actions blindly.
- Record workflow and domain activities.
- Use correlation IDs across API and workflow executions.

## 7. Security boundaries

- HTTPS in deployed environments.
- Secrets only in environment/secret stores.
- Validate all external input.
- Authenticate protected API operations.
- Authorize sales/admin actions by role.
- Protect n8n webhooks/internal endpoints.
- Do not expose provider API keys to React.

## 8. Scalability

Start as a modular monolith. Scale the backend and n8n workers only when actual workload requires it. PostgreSQL indexes and query quality should be addressed before introducing distributed infrastructure.

## 9. Observability

Track request IDs, workflow IDs, lead IDs, errors, durations, AI model/prompt versions, retry counts and notification outcomes. Avoid logging unnecessary sensitive customer content.

## 10. Architecture rules

1. React presents.
2. FastAPI governs.
3. n8n orchestrates.
4. AI interprets/generates.
5. SQL stores authoritative state.
6. Business-critical calculations remain deterministic.
7. No component bypasses validation to write arbitrary business state.
