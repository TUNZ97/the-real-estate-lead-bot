# Documentation — Real Estate Lead Bot

These documents are the **approved source of truth** for product, architecture, contracts and delivery. Read the relevant docs before implementing any feature.

## Core product

| File | Description |
|------|-------------|
| [PRD.md](./PRD.md) | Product requirements, goals, MVP scope |
| [REAL_ESTATE_LEAD_BOT.md](./REAL_ESTATE_LEAD_BOT.md) | Overview, principles, non-goals |
| [SYSTEM_ARCHITECTURE.md](./SYSTEM_ARCHITECTURE.md) | Component boundaries and flows |

## Contracts & domain

| File | Description |
|------|-------------|
| [API_SPECIFICATION.md](./API_SPECIFICATION.md) | HTTP API contracts |
| [DATABASE_DATA_MODEL_SPECIFICATION.md](./DATABASE_DATA_MODEL_SPECIFICATION.md) | PostgreSQL entities, enums, rules |
| [AI_SPECIFICATION.md](./AI_SPECIFICATION.md) | Safe AI usage, extraction schema |
| [LEAD_QUALIFICATION_SPECIFICATION.md](./LEAD_QUALIFICATION_SPECIFICATION.md) | Deterministic scoring & urgency |
| [N8N_WORKFLOW_SPECIFICATION.md](./N8N_WORKFLOW_SPECIFICATION.md) | Workflow list and rules |
| [UI_UX_SPECIFICATION.md](./UI_UX_SPECIFICATION.md) | Customer chat & sales UI |

## Delivery

| File | Description |
|------|-------------|
| [IMPLEMENTATION.md](./IMPLEMENTATION.md) | Phased build plan |
| [DEVELOPMENT_SETUP.md](./DEVELOPMENT_SETUP.md) | Local environment |
| [TESTING_SPECIFICATION.md](./TESTING_SPECIFICATION.md) | Test strategy |
| [DEPLOYMENT_SPECIFICATION.md](./DEPLOYMENT_SPECIFICATION.md) | Environments & release |
| [TASK.md](./TASK.md) | Task template and workflow |

## Rules for contributors & AI agents

1. Do not invent architecture or endpoints not defined here.
2. Prefer the smallest coherent change that satisfies acceptance criteria.
3. Keep AI output validated; business-critical calculations stay deterministic.
4. Update the relevant doc when a contract or behaviour changes.
