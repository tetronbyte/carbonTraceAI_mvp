# 04 — Frontend + API (Current State Checkpoint)

What was built in the Phase-2 sprint after the core calc engine landed: a FastAPI
server that wraps the calc engine, a Next.js 15 frontend that drives the demo
end-to-end, and three backend gap fixes that closed the remaining mapper holes.

> Reading order: this is a **state snapshot** of the new layers. Step-by-step
> setup is in [05_FULL_STACK_SETUP.md](05_FULL_STACK_SETUP.md). Forward roadmap
> is in [06_NEXT_STEPS.md](06_NEXT_STEPS.md).

---

## What's new

```
src/
├── api/                          ★ NEW
│   ├── __init__.py
│   ├── main.py                   FastAPI app — 8 endpoints
│   └── jobs.py                   in-process threaded pipeline runner
├── calculation/
│   ├── engine.py                 ◑ updated — resolve_eua_price() reads live feed
│   └── market_feeds.py           ★ NEW — live EUA override + ECB FX via Frankfurter
└── ingestion/erp/
    ├── erpnext_runner.py         ◑ updated — 3 new stream specs
    └── erp_ingestor.py           ◑ updated — 3 new mappers

frontend/                          ★ NEW (Next.js 15 + Tailwind + Recharts + TanStack Query)
├── package.json
├── tsconfig.json
├── next.config.mjs               proxies /api/* → http://localhost:8000
├── tailwind.config.ts            ink palette + accent glow + glass utility
├── postcss.config.mjs
├── app/
│   ├── layout.tsx                Inter font + radial-gradient bg
│   ├── globals.css
│   ├── providers.tsx             TanStack Query client
│   ├── page.tsx                  landing: profile picker + ERP creds form
│   └── runs/[runId]/
│       ├── layout.tsx            tab nav: Progress · Dashboard · Audit · Reports
│       ├── progress/page.tsx     live step-by-step pipeline + streaming log
│       ├── page.tsx              dashboard: KPIs + donut + SEE bars + tables
│       ├── audit/page.tsx        verifier view: ingestion log + per-line provenance
│       └── reports/page.tsx      XML / CSV / JSON download cards
├── components/ui/
│   ├── Card.tsx
│   ├── Button.tsx
│   └── Badge.tsx
├── lib/
│   ├── api.ts                    typed client for FastAPI endpoints
│   └── format.ts                 fmtTonnes/Eur/Pct + tier colour map
└── README.md

scripts/
└── start_demo.sh                 ★ NEW — one-shot FastAPI + Next.js launcher

requirements.txt                  ◑ +fastapi, +uvicorn[standard], +python-multipart,
                                       +sse-starlette, +httpx
```

★ = brand new · ◑ = modified

---

## The 8 "honest gaps" — status update

From the prior assessment, the eight known soft spots:

| # | Gap | Now | How |
|---|---|---|---|
| 1 | `gl_entries` table populated | ✅ closed | `_map_gl_entry` + new StreamSpec in `erpnext_runner.py` |
| 2 | `stock_movements` table populated | ✅ closed | `_map_stock_entry_item` + new StreamSpec |
| 3 | `outbound_shipments` table populated | ✅ closed | `_map_sales_invoice_item` + new StreamSpec |
| 4 | Live EUA spot price | ✅ env override path | `market_feeds.current_eua_price()` — opt-in via `EngineConfig.use_live_market_feeds=True`; falls back to static |
| 5 | Live FX rates | ✅ live | ECB daily rates via Frankfurter API; verified live: `date=2026-05-13` |
| 6 | XSD-validated XML | 🟡 deferred | Official EU CBAM XSD not yet published by the Commission — slot in `xmlschema.validate()` when it lands |
| 7 | Steel & hydrogen sector runs | 🟡 deferred | Phase 6 in [06_NEXT_STEPS.md](06_NEXT_STEPS.md) |
| 8 | Charts / dashboard UI | ✅ closed | Full Next.js frontend with 5 routes (see below) |

**Net**: 6 of 8 closed, 2 deferred with concrete plans.

---

## API surface — `src/api/main.py`

```
GET  /api/health[?base_url=…]            server probe + ERPNext reachability + market-feed status
GET  /api/profiles                       Mozal / OCP factory profiles + their products
POST /api/runs                           start a pipeline; body {profile_key, base_url, api_key, api_secret, seed_if_empty, fast_demo}
GET  /api/runs                           list all runs (newest first)
GET  /api/runs/{run_id}                  run status — state + steps + log_tail + summaries
GET  /api/runs/{run_id}/dashboard        dashboard JSON (post-success)
GET  /api/runs/{run_id}/xml              CBAM XML download
GET  /api/runs/{run_id}/csv              CBAM CSV download
GET  /api/runs/{run_id}/audit            audit payload — ingestion_events + table_volumes + dashboard + market_feeds
GET  /api/runs/{run_id}/raw-ref?ref=…    drill from canonical row → JSONL source line
```

CORS open for `http://localhost:3000`. Background pipeline runs on a Python thread; state is an in-memory dict (swap for Redis + RQ in production).

The threaded runner in `jobs.py` walks 6 steps:

```
connect_erp  →  seed_erp  →  pull_erp  →  manual_supplement  →  calculate  →  render_reports
```

Each step has `state ∈ {pending, running, succeeded, failed, skipped}` with timestamps + detail line. The frontend polls `/api/runs/{id}` every 800 ms while running.

---

## Frontend — 5 routes

### `/` — landing (profile + ERP creds)

Single screen, two columns:

- **Left**: hero + the two factory profile cards (Mozal aluminium / OCP fertiliser) with sector icon, country, capacity, grid EF, and product list. Click to select; a glow ring marks the active one.
- **Right**: sticky ERP credentials panel. Pre-fills `http://localhost:8080`. ERPNext reachability is polled every 6 s and shown as a coloured dot.
- "Auto-seed if empty" checkbox (fast-demo mode trims the seeder to 3 months × 12 WOs/month so the seed runs in ~90 s).
- **Launch** button → `POST /api/runs` → routes to `/runs/{id}/progress`.

Plus a "Pipeline depth at a glance" 4-card strip — 4 sources, 14 ERP modules, 20 canonical tables, 4 CBAM formulas.

### `/runs/[runId]/progress` — live pipeline

- Left: 6 step rows with state-aware colour (`pending` / `running` / `succeeded` / `failed` / `skipped`) + Lucide icon + start/end timestamps + step-specific detail line (e.g. `"1442 WOs + 956 POs + 144 SInv"`).
- Right: streaming log panel (auto-scrolls to bottom) + per-source ingestion counts as they accrue.
- Bottom: when state = succeeded, a 4-tile verified-output band appears (total tCO₂e, projected CBAM cost, total SEE + adjusted, uncertainty + share-estimated).

The page auto-rerenders on `GET /api/runs/{id}` polled at 800 ms while the run is queued or running; stops polling once the run terminates.

### `/runs/[runId]` — dashboard

The headline screen. Top to bottom:

- **Header band**: facility name + ID + country + sector + quarter pill + estimation-flag pill (amber if any product > 20 % estimated, emerald otherwise).
- **4 KPI tiles**: total emissions / projected CBAM cost / EU export share / energy-grid EF (with sector-aware sub-line: "Hydro advantage" for Mozal, "Grid-EF baseline" for OCP).
- **Charts row**:
  - Emission-split donut (Direct · Indirect · Precursor) with legend.
  - SEE per-product bar chart — pairs total SEE bar with adjusted SEE bar so the carbon-tax deduction is visible.
- **Reconciliation card**: mass-balance / energy-balance / finance cross-check residuals with pass-tolerance badges.
- **Products table**: CN code / name / output / EU exports / total SEE / adj SEE / uncertainty / CBAM cost / est %.
- **Emission-lines table per product**: every line with category dot + label + activity × EF = CO₂e + **tier pill** (measured / supplier_actual / national / cbam_default / ipcc_default / estimated, each colour-coded) + EF source citation + uncertainty.

### `/runs/[runId]/audit` — verifier view

The depth view — what proves the platform isn't a black box:

- **Ingestion depth banner**: 5 source-type tiles (ERP / MANUAL / METER / SUPPLIER / INVOICE), each showing how many canonical rows came from that source.
- **Canonical store table volumes**: every one of the 20 tables with row count, dimmed when empty so the next dev can see at a glance what's modelled-but-not-flowing.
- **`ingestion_events` log**: every sync stamped with source / stream / records / OK / errors / started-at — immutable audit ledger.
- **Per-line provenance cards** for the first product: each emission line as its own card with the activity × EF computation expanded, tier pill, source citation, uncertainty.
- **"Replayability" panel**: 5 numbered items spelling out the audit-trail story (raw JSONL preserved → `raw_ref` back-pointer → ERPNext records browsable → ingestion_events ledger → CBAM XML signed).

### `/runs/[runId]/reports` — downloads

- 3 download cards (XML / CSV / JSON), each with a feature checklist of what's inside.
- Headline numbers grid (8 tiles): total / direct / indirect / precursor / projected CBAM / EU export share / product count / estimation flag count.
- "Next step" panel: EU CBAM portal upload + verifier sign-off explanations.
- Footer: "All artefacts stored locally at `data/reports/` — never leaves your machine."

---

## Verified end-to-end status

| Check | Result |
|---|---|
| `pytest tests/` | **30 passed** in 1.4 s — all original tests still green |
| `npx tsc --noEmit` (frontend) | clean — no type errors |
| `npm run build` | clean — 4 dynamic routes + 1 static page, 102 kB shared JS |
| `curl /api/health` | `{"status":"ok", "market_feeds":{"fx_source":"ECB via Frankfurter (date=2026-05-13)"}}` |
| `curl /api/profiles` | returns both Mozal + OCP with full product lists |
| `curl /api/runs` | empty list initially; populated after `POST /api/runs` |

---

## Design language

- **Palette**: dark base (`ink-900` zinc-950 equivalent) + indigo accent (`#6366f1`) + emerald positive (`#34d399`) + amber warning + rose error.
- **Body backdrop**: 3 stacked radial gradients (indigo glow top-left, emerald glow top-right, indigo glow bottom-centre) — fixed-attachment so the gradient doesn't scroll.
- **Cards**: `glass` utility = `bg-ink-800/60 backdrop-blur-xl border border-white/5`. Rounded-xl.
- **Typography**: Inter via `next/font` with `cv11` + `ss01` features, font-feature settings tuned for monospace-feeling numerics.
- **Icons**: Lucide React (`lucide-react`).
- **Charts**: Recharts. Tooltip styled to match the card glass.
- **State indicators**: subtle pulse on running, soft-glow ring on selection, never harsh.
- **Tier colour coding** in `lib/format.ts` — applied identically across dashboard, audit view, and reports so a "supplier-actual" line looks the same wherever it appears.

---

## What's still soft (for the next sprint)

- **No Sankey chart yet** — precursors → process → product flow would visualise the calc engine's complex-goods math. Recharts has primitives; a custom SVG d3-sankey component is ~1 day.
- **No multi-facility switcher** — dashboard renders `facilities[0]`. Add a tab/select once we have a 2-facility demo.
- **No raw_ref deep-link UI** — `/api/runs/{id}/raw-ref?ref=...` works server-side; the audit page doesn't yet wire a click-through. ~2 hours.
- **No PDF report** — the three downloads cover audit submission (XML) and BI (CSV/JSON), but the "board-pack" PDF flavour from the roadmap isn't here yet.
- **No auth** — landing page is open. For the YC demo this is fine; for any external pitch through ngrok wrap with HTTP basic via FastAPI middleware (5-line change) or move to Clerk for SSO.
- **Polling instead of SSE** — 800 ms poll is fine for the demo cadence (~30 s end-to-end). `sse-starlette` is in requirements.txt for the moment it matters.

Everything above is in [06_NEXT_STEPS.md](06_NEXT_STEPS.md) with priority + effort estimates.
