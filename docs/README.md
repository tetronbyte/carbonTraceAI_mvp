# carbonTraceAI — Handover Documentation

Read these in order if you're picking this up cold. **Docs 1–3** cover the
backend pipeline + calc engine. **Docs 4–6** are the post-Phase-2 docs covering
the FastAPI server + Next.js frontend.

### Backend / calc engine (Phase 1)

| # | Doc | What it covers |
|---|---|---|
| 1 | [01_OUTPUTS.md](01_OUTPUTS.md) | Every artefact the pipeline produces — ERPNext records, raw JSONL, canonical SQLite, CBAM XML/CSV/JSON. Sample volumes + sample content. |
| 2 | [02_SETUP_AND_RUN.md](02_SETUP_AND_RUN.md) | Backend-only setup. Boot ERPNext, seed, ingest, calculate. Smoke-test path with no Docker. |
| 3 | [03_ROADMAP.md](03_ROADMAP.md) | Original calc-engine-only roadmap — superseded by `06_NEXT_STEPS.md`. Kept for context. |

### Frontend + API (Phase 2 — current state)

| # | Doc | What it covers |
|---|---|---|
| 4 | [04_FRONTEND_AND_API.md](04_FRONTEND_AND_API.md) | Current-state checkpoint — what the FastAPI server exposes, what the 5 Next.js routes show, status of the 8 prior "honest gaps". |
| 5 | [05_FULL_STACK_SETUP.md](05_FULL_STACK_SETUP.md) | **The full-stack setup guide.** 5 commands from a clean machine to `localhost:3000`. Sample admin creds + demo walkthrough + troubleshooting. |
| 6 | [06_NEXT_STEPS.md](06_NEXT_STEPS.md) | **The current roadmap.** Honest assessment of "is the frontend complete?", calc-engine robustness Phase A + B, ERP-fidelity gaps, productionisation, sector expansion, 8-week build plan. |

The top-level [`README.md`](../README.md) is the project overview. The CLAUDE-style automatic memory in `/Users/<you>/.claude/projects/.../memory/` carries the why-decisions (pivot history, audit-funder audience, CBAM estimation rules).

## Quick orientation

```
carbonTraceAI_mvp/
├── docs/                       ← you are here
├── config/                     CBAM data dictionary, grid EFs
├── src/
│   ├── core/                   Pydantic models, enums, base ingestor
│   ├── storage/                SQLite Repository (20 tables)
│   ├── ingestion/
│   │   ├── erp/                ERPNext client + runner (incl. gl/stock/sales mappers)
│   │   ├── manual/             facility / sensor / supplier portal forms
│   │   └── ocr/                pdfplumber + Tesseract invoice extraction
│   ├── onboarding/             connector registry + Fernet vault + factory
│   ├── seeding/                FactoryProfile + ERPNextSeeder v2
│   ├── calculation/            CBAM calc engine (formulas, allocation, market feeds)
│   ├── api/                    ★ FastAPI server (8 endpoints + threaded job runner)
│   └── utils/                  logger, JSONL landing zone
├── frontend/                   ★ Next.js 15 + Tailwind + Recharts + TanStack Query
│   ├── app/                    5 routes: landing / progress / dashboard / audit / reports
│   ├── components/             shared UI primitives + cards
│   └── lib/                    typed API client + formatters
├── scripts/                    one-shot CLIs + start_demo.sh launcher
├── tests/                      30 smoke tests (all green)
└── docker-compose.erpnext.yml  ERPNext sandbox
```
