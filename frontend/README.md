# Frontend — React (Vite + TypeScript)

Customer chat and sales dashboard for PrimeHomes Real Estate Lead Bot.

See [docs/UI_UX_SPECIFICATION.md](../docs/UI_UX_SPECIFICATION.md).

## Run locally

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173  
API proxy: `/api` and `/health` → `http://localhost:8000`

## Structure (planned)

```text
src/
├── components/     # Chat, Message, Loading, forms
├── pages/          # Customer chat, Sales dashboard, Lead detail
├── hooks/
├── api/            # typed API client
├── types/
├── App.tsx
└── main.tsx
```

Implementation order (from IMPLEMENTATION.md):

Customer chat → API integration → lead dashboard → lead detail → status/actions → follow-up → polish.
