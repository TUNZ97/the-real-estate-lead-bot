# Tests

Cross-cutting and end-to-end tests. Unit and integration tests for each component also live closer to the code (`backend/tests`, `frontend` test scripts) as they are added.

See [docs/TESTING_SPECIFICATION.md](../docs/TESTING_SPECIFICATION.md).

```text
tests/
├── backend/          # API / integration (or use backend/tests)
├── e2e/              # End-to-end scenarios
├── fixtures/         # Shared fixtures, golden AI cases
└── README.md
```

E2E scenarios (from the testing spec) include detailed buy enquiries, incomplete follow-ups, duplicate messages, high-urgency notifications, human handoff, viewing requests, follow-up due, AI failures, and conversion/loss paths.
