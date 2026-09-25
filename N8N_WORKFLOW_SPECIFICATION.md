# n8n Workflow Specification

## 1. Purpose

Define the n8n workflows that orchestrate AI processing, integrations, notifications and scheduled automation.

## 2. Boundary

n8n orchestrates. FastAPI owns authoritative business rules and database operations. n8n must not become a second backend containing undocumented domain logic.

## 3. Workflows

### WF-001 Lead Intake
Receive/route a message event, validate payload, check idempotency, call backend/AI processing, persist results and trigger next workflow.

### WF-002 Lead Qualification
Consume validated lead data, invoke deterministic backend qualification, record the result and route high-priority cases.

### WF-003 Customer Response
Build grounded response context, call AI response generation, validate the result, send response and record the message.

### WF-004 Sales Notification
Evaluate notification rules, format the lead summary, send to configured sales channel and record delivery state.

### WF-005 Human Handoff
Handle explicit/automatic escalation, notify/assign sales, update conversation/lead state and stop conflicting bot automation.

### WF-006 Follow-Up Reminder
Scheduled workflow finds due follow-ups, verifies lead state, sends reminder or creates an agent task, then records outcome.

### WF-007 Lead Status Sync
Synchronize approved status changes with connected systems without creating conflicting sources of truth.

### WF-008 Conversation Summary
Generate/update a concise sales summary from validated conversation context.

### WF-009 Error Handler
Capture failed executions, classify transient vs permanent errors, retry safe operations and notify operators for unresolved failures.

### WF-010 Scheduled Maintenance
Perform housekeeping tasks such as overdue follow-up marking, safe cleanup and operational checks.

## 4. Standard workflow structure

```text
Trigger → Validate → Idempotency → Fetch Context → Process
→ Backend Validation → Action → Persist Activity → Notify/Continue
```

## 5. AI workflow rules

- Validate structured AI output.
- Never let raw AI output directly perform privileged actions.
- Keep prompt/model versions traceable.
- Handle provider timeout/rate-limit/schema failures.
- Use only relevant conversation context.

## 6. Deterministic vs AI

AI: language interpretation and response generation.

Backend: qualification score, lifecycle transitions, authorization and database truth.

n8n: routing, scheduling, integration and workflow control.

## 7. Reliability

Use timeouts, retries for transient failures, idempotency for repeated events and explicit dead/error handling. Avoid infinite retries.

## 8. Security

Protect webhooks, credentials and internal callbacks. Validate incoming payloads. Do not expose secrets in execution data or logs unnecessarily.

## 9. Node guidance

Use visual nodes for straightforward routing/transformation. Use Code nodes only for transformations that are genuinely clearer or unavailable in standard nodes. Use If/Switch for explicit routing, Merge for controlled aggregation and Wait for scheduled follow-up behavior.

## 10. Testing

Every workflow needs representative success, validation-failure, external-failure and duplicate-event cases. Critical workflows need recovery/retry verification.

## 11. Versioning

Export workflows to the repository or otherwise maintain version-controlled definitions and documented credentials/configuration requirements. Keep workflow names stable and descriptive.

## 12. Implementation order

WF-001 → WF-002 → WF-003 → WF-004 → WF-005 → WF-006 → WF-007 → WF-008 → WF-009 → WF-010.

## 13. Definition of Done

The workflow is documented, importable, configured for the target environment, authenticated, tested against failure cases, observable and integrated with the documented API contracts.
