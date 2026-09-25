# Task Specification

## 1. Purpose

Provide a consistent task system for implementing the Real Estate Lead Bot and coordinating human and AI coding work.

## 2. Statuses

`BACKLOG` → `READY` → `IN_PROGRESS` → `IN_REVIEW` → `TESTING` → `DONE`

Exceptions: `BLOCKED`, `CANCELLED`.

## 3. Priorities

- **P0:** critical/MVP blocker.
- **P1:** core MVP.
- **P2:** important but not blocking MVP.
- **P3:** future/improvement.

## 4. Task types

Feature, bug, refactor, documentation, infrastructure, database, AI, n8n, frontend, backend, testing.

## 5. Task template

```markdown
## TASK-XXX — Short title

**Status:** READY
**Priority:** P1
**Owner:**
**Type:**
**Dependencies:**

### Goal

### Context

### Requirements

### Acceptance Criteria
- [ ]

### Implementation Notes

### Tests

### Related Docs
```

## 6. Definition of Ready

A task has a clear outcome, scope, acceptance criteria, dependencies, relevant specification references and enough context for implementation.

## 7. Definition of Done

Code/documentation is complete, tests pass, acceptance criteria are met, security implications are considered and the change is reviewable.

## 8. Dependency rules

Do not start a task whose prerequisite contract/schema is undefined unless the task explicitly includes defining it. Prefer dependency chains over hidden assumptions.

## 9. AI coding agent rules

An AI agent must read the relevant docs before editing code, inspect existing implementation, make focused changes, run tests, report failures honestly and avoid creating duplicate abstractions.

## 10. Examples

- `DB-001` Create initial schema.
- `BE-001` Implement message intake API.
- `AI-001` Implement extraction schema and provider adapter.
- `N8N-001` Implement lead intake workflow.
- `FE-001` Build customer chat.
- `QA-001` Add end-to-end lead flow.
- `OPS-001` Configure staging deployment.

## 11. MVP workstream

Foundation → database → backend → AI → n8n → qualification → customer UI → sales UI → follow-up → testing → deployment.

## 12. Progress reporting

Each task should communicate current status, completed work, blockers, next step and relevant tests. Avoid reporting percentage complete without concrete evidence.

## 13. Commit/PR guidance

Keep commits focused. Reference task IDs. PRs should explain behavior changes, tests, migration impact and any configuration changes.
