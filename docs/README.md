# carbonTraceAI — Handover Documentation

Read these three in order if you're picking this up cold:

| # | Doc | What it covers |
|---|---|---|
| 1 | [01_OUTPUTS.md](01_OUTPUTS.md) | Every artefact the pipeline produces — ERPNext records, raw JSONL, canonical SQLite, CBAM XML/CSV/JSON. Sample volumes + sample content. |
| 2 | [02_SETUP_AND_RUN.md](02_SETUP_AND_RUN.md) | Step-by-step from a clean machine: install, boot ERPNext, seed, ingest, calculate, troubleshoot. |
| 3 | [03_ROADMAP.md](03_ROADMAP.md) | Forward path — gaps, calc-engine hardening, dashboard (Next.js + Tremor), report generation, productionisation, sector expansion. |

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
│   │   ├── erp/                ERPNext client, runner, Airbyte stub
│   │   ├── manual/             facility / sensor / supplier portal forms
│   │   └── ocr/                pdfplumber + Tesseract invoice extraction
│   ├── onboarding/             connector registry + Fernet vault + factory
│   ├── seeding/                FactoryProfile + ERPNextSeeder v2
│   ├── calculation/            CBAM calc engine (formulas, allocation,
│   │                            uncertainty, renderer)
│   └── utils/                  logger, JSONL landing zone
├── scripts/                    one-shot CLIs
├── tests/                      30 smoke tests
└── docker-compose.erpnext.yml  ERPNext sandbox
```
