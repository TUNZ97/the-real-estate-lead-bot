# API Specification

## 1. Purpose

Define the stable HTTP API between the frontend, external clients, automation workflows and FastAPI backend.

Base path: `/api`.

## 2. Conventions

- JSON request/response bodies.
- ISO-8601 timestamps in UTC.
- Stable resource IDs.
- Pagination for collection endpoints.
- Validation errors return structured details.
- Authentication required for protected sales/admin endpoints.
- API versioning should be introduced when breaking changes are unavoidable.

## 3. Core endpoints

### Messages
`POST /api/messages` — submit a customer message.

Example request:
```json
{"conversation_id":"conv_123","message":"I need a 3-bedroom apartment in Lekki"}
```

Example response:
```json
{"conversation_id":"conv_123","message_id":"msg_456","response":"Thanks! Are you looking to buy or rent?","lead_id":"lead_789"}
```

### Leads
- `GET /api/leads`
- `GET /api/leads/{lead_id}`
- `PATCH /api/leads/{lead_id}`
- `POST /api/leads/{lead_id}/status`
- `POST /api/leads/{lead_id}/qualify`

### Conversations
- `GET /api/conversations/{conversation_id}`
- `GET /api/conversations/{conversation_id}/messages`

### Follow-ups
- `POST /api/leads/{lead_id}/follow-ups`
- `GET /api/leads/{lead_id}/follow-ups`
- `PATCH /api/follow-ups/{follow_up_id}`

### Notifications
- `GET /api/notifications`
- `POST /api/notifications/{id}/acknowledge`

### Health
- `GET /health`
- `GET /ready`

## 4. Error format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": []
  },
  "request_id": "req_123"
}
```

Do not expose stack traces or provider secrets.

## 5. Authentication and authorization

Use a standard token/session mechanism for protected internal APIs. Roles determine access to sales and admin operations. Customer-facing message intake may use a separate channel authentication mechanism.

## 6. Idempotency

Message intake must support an external message identifier or idempotency key. Repeated delivery of the same event must not create duplicate messages/leads or duplicate irreversible notifications.

## 7. Validation

Pydantic models validate syntax and field types. Domain services validate business rules such as legal status transitions, budget ranges and ownership.

## 8. Pagination/filtering

List endpoints should support explicit page/limit or cursor semantics and filters such as status, qualification, urgency, assigned user and date range.

## 9. n8n integration

Internal workflow callbacks must be authenticated and should carry stable identifiers such as `lead_id`, `conversation_id`, `message_id` and correlation/request IDs. n8n should call documented backend operations rather than directly manipulating database tables.

## 10. API change policy

- Additive changes are preferred.
- Breaking changes require versioning/migration planning.
- Update tests and documentation with contract changes.
- Do not let AI coding agents invent undocumented endpoints.
