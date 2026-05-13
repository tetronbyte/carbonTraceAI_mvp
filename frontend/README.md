# carbonTraceAI Frontend

Next.js 15 + Tailwind + TanStack Query + Recharts. Talks to the FastAPI server
at `:8000` (proxied through `/api/*` via `next.config.mjs`).

## Run

```bash
# 1. Backend (FastAPI)
cd ..
source .venv/bin/activate
uvicorn src.api.main:app --reload --port 8000

# 2. Frontend (Next.js)
cd frontend
npm install
npm run dev
# open http://localhost:3000
```

## Pages

| Route | What |
|---|---|
| `/` | Profile selection + ERP credential form (sample admin creds pre-filled) |
| `/runs/[runId]/progress` | Live pipeline progress with step-by-step status + streaming log |
| `/runs/[runId]` | Dashboard — KPIs, emission split donut, SEE bars, reconciliation, products + emission lines |
| `/runs/[runId]/audit` | Verifier view — ingestion event log, table volumes, per-line provenance |
| `/runs/[runId]/reports` | Downloadable XML / CSV / JSON + headline numbers + next-step guidance |

## Notes

- Polling-based progress (800 ms while running). SSE could be plugged in
  later via `sse-starlette` on the backend.
- Sample administrator creds are not embedded in source. The first seed run
  writes `.env.erpnext` at the repo root; copy the API key + secret from there
  into the form.
- The frontend is read-only against `/api`. No direct DB or filesystem access.

## Design language

- Dark base (`ink-900`) + indigo/emerald accents
- Inter font with `cv11` + `ss01` features
- Subtle radial-gradient body backdrop
- `glass` utility class for cards
- Tier-aware color coding (measured = emerald, IPCC = amber, estimated = rose)
