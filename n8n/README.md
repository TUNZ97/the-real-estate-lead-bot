# n8n Workflows

Exported workflow definitions for the Real Estate Lead Bot.

n8n **orchestrates**; FastAPI owns business rules and the database. See [docs/N8N_WORKFLOW_SPECIFICATION.md](../docs/N8N_WORKFLOW_SPECIFICATION.md).

## Planned workflows

| ID | Name | Phase |
|----|------|-------|
| WF-001 | Lead Intake | 5 |
| WF-002 | Lead Qualification | 5 |
| WF-003 | Customer Response | 5 |
| WF-004 | Sales Notification | 5 |
| WF-005 | Human Handoff | 5 |
| WF-006 | Follow-Up Reminder | 5 |
| WF-007 | Lead Status Sync | later |
| WF-008 | Conversation Summary | later |
| WF-009 | Error Handler | 5 |
| WF-010 | Scheduled Maintenance | later |

## Directory

```text
n8n/
├── workflows/     # JSON exports (version-controlled)
└── README.md
```

Import workflows into a local n8n instance after configuring credentials and webhook secrets from `.env`.
