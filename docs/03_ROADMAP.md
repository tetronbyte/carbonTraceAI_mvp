# 03 — Roadmap: From MVP to YC-Ready Product

Where this codebase is today, what's still soft, and the build order to get to a defensible commercial product.

---

## Current state (as of handover)

**Solid**:
- Real ERP system of record (ERPNext) with FK-coherent masters + transactionals
- Stoichiometrically-coherent seeder for 2 factory profiles (Mozal aluminium, OCP fertiliser)
- 4-source ingestion: ERPNext REST or Airbyte, manual, supplier portal, OCR
- 20-table canonical Pydantic store
- Full CBAM calc engine: IPCC + Annex defaults, EF priority, uncertainty propagation, coproduct allocation, REC offset, Block-G carbon-price-paid deduction, mass/energy/finance reconciliation
- Three output renderers: EU CBAM XML, dashboard CSV, dashboard JSON
- 30 passing smoke tests
- Onboarding framework (vault + connector registry + Airbyte provisioner) for 8 ERP connectors

**Not yet (the rest of this doc)**:
- Web UI / dashboard
- FastAPI server + Postgres multi-tenant
- PDF report generator
- Stock-movement / GL-entry / outbound-shipment ingestion mappers
- Live FX + EUA spot price feeds
- Steel + hydrogen sector branches
- Auth + billing
- Behaviour-faithful simulator hardening (campaign cycles, batch-level material traceability)
- Sales onboarding wizard
- SOC 2 prep

---

## Phase 1 — Close the calc-engine soft spots (~1 week)

These are additive — no architectural changes.

| # | Gap | What to build | Files to touch |
|---|---|---|---|
| 1.1 | **Stock-entry ingestion** | Mapper in `ERPNextRunner.STREAM_SPECS` for the `Stock Entry` doctype → `StockMovement` canonical model. Closes the three-way audit chain (PO → GR → Invoice) for the verifier. | `src/ingestion/erp/erpnext_runner.py`, `src/ingestion/erp/erp_ingestor.py` |
| 1.2 | **GL-entry ingestion** | Same pattern for `GL Entry` → `GLEntry` canonical. Enables the `finance_cross_check` reconciliation to actually fire. | same |
| 1.3 | **Sales Invoice → OutboundShipment mapper** | Pull `Sales Invoice` rows, derive port-of-loading from facility UN-LOCODE, port-of-discharge from EU customer country, sea distance from the lookup. | same |
| 1.4 | **Live EUA + FX feeds** | Replace static `EUA_PRICE_EUR_PER_TCO2E` and `FX_TO_EUR` with HTTP fetchers (ICE for EUA, ECB for FX). Cache 24h. | `src/calculation/lookup_tables.py` + new `src/calculation/market_feeds.py` |
| 1.5 | **Campaign-cycle time-series** | The seeder has monthly granularity. Add intra-month potline ramps (12h cycles) and SMR campaign starts/stops. | `src/seeding/erpnext_seeder.py` |
| 1.6 | **Stoichiometric driver tightening** | The current `±5%` noise in PO sizing → tighten to `±2%` and add a verification step that asserts month-over-month mass balance within tolerance. | `src/seeding/erpnext_seeder.py` |
| 1.7 | **BOM-level scrap accounting** | Today scrap is a rate field. Make it deduct from finished output AND emit a `StockMovement` for the scrap qty. | `src/seeding/erpnext_seeder.py` |
| 1.8 | **EF library expansion** | `CBAM_DEFAULT_EMBEDDED` has 12 CN codes. Bulk-load the full Annex VIII CSV from the EU Commission (~50 codes) when published. | `src/calculation/lookup_tables.py` |
| 1.9 | **Reconciliation tolerance config** | Move the 5% / 10% / 2% tolerances out of hardcoded params into per-facility `MonitoringMeta`. | `src/core/models.py` + `engine.py` |

**Acceptance test**: after Phase 1, the calc engine produces zero `🟡 modeled` rows in the CBAM checklist for any sector in MVP scope, and `finance_cross_check` returns a real residual (not None).

---

## Phase 2 — Web UI / dashboard (YC-startup-level, ~3 weeks)

**Stack** (deliberately opinionated):

| Layer | Tool | Why |
|---|---|---|
| Framework | Next.js 15 (App Router, TypeScript) | Industry standard, server components, RSC streaming |
| Styling | Tailwind CSS + shadcn/ui | Fast, polished, accessible |
| Charts | [Tremor](https://www.tremor.so/) (built on Recharts) | Pre-built dashboard primitives — KPI cards, area charts, donut, sparklines |
| Tables | TanStack Table v8 | Server-side pagination, column groups, sticky headers |
| Maps | Mapbox GL JS or MapLibre | Facility map + grid-EF heatmap |
| Sankey | `react-flow` or `d3-sankey` | Precursor → process → product emission flows |
| Auth | [Clerk](https://clerk.com) (drop-in) or Supabase Auth (self-hosted) | SSO ready, magic links, MFA |
| Forms | React Hook Form + Zod | Same Pydantic shapes on both sides |
| API client | TanStack Query + generated OpenAPI client | Auto-typed from FastAPI |
| Deploy | Vercel (frontend) + Fly.io (API + Postgres) | Zero-config CI/CD, EU regions for data residency |

### Routes / pages

```
/                                          → marketing landing
/dashboard                                 → org-level overview
/dashboard/facilities                      → facility list
/dashboard/facilities/[facility_id]        → per-facility detail
/dashboard/facilities/[id]/products/[cn]   → per-product drill-down
/dashboard/runs                            → all calculation runs (history)
/dashboard/runs/[run_id]                   → single run detail + XML/CSV/PDF downloads
/dashboard/connectors                      → connector registry + onboarding wizard
/dashboard/connectors/[connection_id]      → sync status + creds management
/dashboard/data-quality                    → estimation flags, uncertainty, reconciliation
/dashboard/settings/facility/[id]          → manual forms (facility metadata, MR Plan, RECs, etc.)
/dashboard/audit/[run_id]                  → verifier view (every line, every source)
```

### Per-facility detail page (the headline screen)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Mozal Aluminium SA — MOZAL-MZ-01 — Mozambique                       │
│  Quarter ▼ 2026-Q2          Last sync: 2h ago     [Re-sync] [Export ⌄]│
├──────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────────┐  │
│  │ Total tCO2e  │ │ CBAM cost €  │ │ EU export %  │ │ Data quality│  │
│  │   204,207    │ │  6,738,840   │ │     60.0%    │ │  ⚠ 36% est. │  │
│  │  ▲ 4% QoQ    │ │  ▲ €420k QoQ │ │  ▲ 2pp QoQ   │ │  >20% flag  │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └─────────────┘  │
│                                                                       │
│  ┌──── Emissions breakdown ────┐  ┌──── SEE per product ────────┐    │
│  │  [stacked donut]            │  │  [horizontal bar chart]      │    │
│  │  Direct   81,407 (40%)      │  │  76011000 — 4.084 tCO2e/t   │    │
│  │  Indirect 22,000 (11%)      │  │  ─adj─    2.995 tCO2e/t     │    │
│  │  Precur  100,800 (49%)      │  │  EUA: €75/t                 │    │
│  └─────────────────────────────┘  └──────────────────────────────┘    │
│                                                                       │
│  ┌──── Emission flow (Sankey) ────────────────────────────────────┐  │
│  │  Alumina      ───100.8k──┐                                     │  │
│  │  Anode        ───74.2k───┤                                     │  │
│  │  PFCs         ───7.2k────┼─── Primary Al ingot ─── 30k t to EU │  │
│  │  Grid power   ───22k─────┤                                     │  │
│  │  Refrigerant  ───<1k─────┘                                     │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌──── Reconciliation health ────────────────────────────────────┐   │
│  │  Mass balance        ✓  residual 3.2% (tolerance 5%)          │   │
│  │  Energy balance      ✓  residual 5.8% (tolerance 10%)         │   │
│  │  Finance cross-check ⚠  GL entries not yet ingested            │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌──── Emission lines (with provenance) ─────────────────────────┐   │
│  │  Category  Label                 EF source         Tier    %   │   │
│  │  process   Pre-bake anode CO2    IPCC V3 Ch4 Eq 4. ipcc 36.3%  │   │
│  │  process   PFCs (CF4 + C2F6)     IPCC V3 Ch4 T1    ipcc  3.5%  │   │
│  │  electric  Grid (potline_1)      MZ national EF    natnl 10.8% │   │
│  │  precurs   Alumina (CN 28182000) Alunorte declared suplr 49.4% │   │
│  └────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

Every chart has a click-through that filters the line table.

### Data layer

Backend exposes:
```
GET  /api/runs                        list calculation runs
GET  /api/runs/{run_id}               full CalculationRun JSON
GET  /api/runs/{run_id}/xml           CBAM XML (passthrough)
GET  /api/runs/{run_id}/csv           CSV (passthrough)
GET  /api/runs/{run_id}/pdf           rendered PDF report
GET  /api/facilities                  list facilities
GET  /api/facilities/{id}/emissions?quarter=2026-Q2
POST /api/runs/trigger                start a calc run (background job)
POST /api/connectors                  onboard a new connection
POST /api/connectors/{id}/sync        trigger sync
GET  /api/audit/ingestion-events      paginated event log
```

The frontend never touches SQLite directly. All read paths go through FastAPI; all write paths require auth.

### Specific charts to ship

| Chart | Library | Data source |
|---|---|---|
| KPI tile (current quarter) | Tremor `Card` | `facility.totals.*` |
| QoQ trend sparkline | Tremor `SparkAreaChart` | rolling-window query on Repository |
| Emissions breakdown donut | Tremor `DonutChart` | `direct / indirect / precursor` |
| Per-product SEE bars | Tremor `BarChart` | `products[].totalSEE` |
| Emission-source Sankey | `d3-sankey` + custom React | `products[].lines` aggregated |
| Facility map | Mapbox GL JS | facility GPS + grid EF colour |
| Reconciliation status cards | shadcn `Alert` | `reconciliation.*` |
| Estimation-flag panel | shadcn `Badge` + `Tooltip` | `estimationFlags` |
| Drill-down line table | TanStack Table | `products[].lines` |

### Audit view (separate page for verifiers)

Sole purpose: prove every number. Per CN code, show:
1. The emission-lines table (with EF source citation)
2. Click a line → modal showing the canonical Pydantic row
3. Click the row's `raw_ref` → opens the JSONL line + a deep-link to the ERPNext document
4. Reconciliation residuals + tolerances + pass/fail badges
5. MR Plan PDF download
6. Verification report PDF download
7. Signed audit-trail PDF (next phase)

---

## Phase 3 — Report generation (PDF) (~1 week)

PDF is the artefact the operator emails to their EU declarant and the verifier prints.

**Stack options**:
- **WeasyPrint** (Python, HTML+CSS → PDF) — recommended; reuses the same templates the dashboard renders
- **ReportLab** (Python, programmatic) — more control, more work
- **jsPDF** (browser-side) — simpler but less reliable for multi-page tables

Recommended layout:

```
Page 1 — Cover                Plant name, logo, reporting period, declarant info, sign-off block
Page 2 — Executive summary    KPI tiles, headline chart
Page 3-4 — Per-product detail One per CN code: SEE table + emission-line breakdown
Page 5 — Reconciliation       Mass / energy / finance residuals with explanations
Page 6 — Estimation methods   Per-product share-estimated + 20% threshold flags
Page 7 — Audit trail          Ingestion events, sync timestamps, EF source citations
Page 8 — Appendices           Method references (IPCC tables, CBAM Annex VIII)
```

API endpoint:
```
GET /api/runs/{run_id}/pdf?style=audit   → audit PDF
GET /api/runs/{run_id}/pdf?style=board   → board-pack PDF (fewer pages, exec summary)
GET /api/runs/{run_id}/pdf?style=declarant → for the EU importer
```

Template file structure (suggested):
```
src/calculation/templates/
├── pdf_audit.html
├── pdf_board.html
├── pdf_declarant.html
└── styles/cbam.css
```

Each template gets the `CalculationRun` Pydantic object as `run`. Jinja2 + Tailwind-equivalent CSS works well.

---

## Phase 4 — Productionise the backend (~2 weeks)

### From SQLite to Postgres

```python
# config/settings.py — already supports this via env
CARBONTRACE_DB_URL=postgresql+psycopg://carbontrace:****@db.fly.dev/carbontrace
```

SQLAlchemy handles the dialect switch. Things to do:
1. Generate Alembic migrations from current models: `alembic init alembic && alembic revision --autogenerate -m init`
2. Add a `tenant_id` UUID column on every table
3. Enable Postgres Row-Level Security (RLS) — per-tenant filter via session GUC
4. Index the hot columns: `(tenant_id, facility_id, period_start)`

### FastAPI server

```
src/api/
├── main.py              FastAPI app + middleware
├── deps.py              dependency injection (auth, tenant, repo)
├── routes/
│   ├── runs.py          /api/runs/*
│   ├── facilities.py    /api/facilities/*
│   ├── connectors.py    /api/connectors/*
│   ├── manual.py        /api/manual/* (form submissions)
│   └── audit.py         /api/audit/*
├── schemas.py           Pydantic request/response shapes
└── jobs.py              long-running tasks (sync, calc) → RQ
```

Auth middleware: validate Clerk JWT → resolve `tenant_id` → set Postgres session GUC.

### Background jobs

ERPNext seeds and full pipeline runs are too slow for HTTP. Use [RQ](https://python-rq.org/) (simpler) or Celery (more features) backed by Redis.

```python
# scripts.seed_erpnext invoked from a job
from rq import Queue
queue = Queue("seeds", connection=redis)
job = queue.enqueue("scripts.seed_erpnext.run_profile", profile="mozal_aluminium")
# poll job.status from the frontend
```

### Observability

- Sentry for errors (frontend + backend)
- OpenTelemetry traces (FastAPI middleware)
- Structured logs (`structlog`) to stdout
- Dashboards: Grafana Cloud free tier, or Vercel/Fly built-ins

### CI/CD

`.github/workflows/ci.yml`:
- lint (ruff)
- type-check (mypy)
- pytest
- build Docker image
- deploy preview to Fly.io on PR
- deploy to prod on merge to main

---

## Phase 5 — Multi-tenancy + Auth + Billing (~2 weeks)

### Multi-tenant from day one

Every table needs `tenant_id`. The cleanest pattern:

```sql
CREATE POLICY tenant_isolation ON production_runs
  USING (tenant_id = current_setting('app.current_tenant')::uuid);
ALTER TABLE production_runs ENABLE ROW LEVEL SECURITY;
```

FastAPI middleware reads the Clerk JWT, fetches `tenant_id`, sets the Postgres GUC before any query.

### Auth

**Clerk** (recommended for speed): SSO (Google, Microsoft, Okta), magic links, MFA, organisation switcher, user invitations. 5-line drop-in.

**Self-hosted alternative**: Supabase Auth or Authentik — more compliance flexibility, more ops overhead.

### Billing

Stripe — usage-based pricing. Charge per `(facility × quarter)` or per CBAM certificate value tracked.

```
Free tier:  1 facility, 50 work orders/month, no PDF report download
Growth:     €499/facility/month, unlimited records, PDF + XML downloads
Enterprise: custom — multi-region hosting, SSO, dedicated CSM
```

Stripe Customer Portal handles self-service upgrade/downgrade. Map Stripe subscription → tenant feature flags.

---

## Phase 6 — Sector expansion (~1 week each)

The calc engine is sector-aware via the `Sector` enum + per-sector process line generators. Adding a sector means:

1. Add CN codes + factory profile in `src/seeding/factory_profiles.py`
2. Add CBAM Annex VIII defaults in `src/calculation/lookup_tables.CBAM_DEFAULT_EMBEDDED`
3. Add process-emission estimators in `src/calculation/estimators.py`
4. Add a `_<sector>_process_lines` method in `src/calculation/engine.py`
5. Add tests in `tests/test_calculation.py`

### Sectors prioritised by CBAM cost exposure for African clients

| Sector | CN codes | Process emissions to model | Effort |
|---|---|---|---|
| **Steel** (D1) | 7201 / 7207 / 7208 / 7213 / 7301 | Coke as reductant, BFG/BOF gas, limestone calcination, pig iron / DRI / scrap precursors | ~1 week |
| **Cement** (clinker) | 2523 | Clinker calcination CO2, alternative fuels | ~3 days |
| **Hydrogen** | 2804 | SMR / ATR / electrolysis pathways, CCS credit, water consumption (electrolysis efficiency) | ~3 days |
| **Lime / iron ore** | 2521 / 2601 | Calcination, ore beneficiation electricity | ~2 days |

---

## Phase 7 — Compliance & verification (~ongoing)

### SOC 2 Type II prep

Drata or Vanta — automated control monitoring. Start in parallel with paying customers.

Key controls to put in code:
- All secrets in vault (Clerk metadata + Fernet at-rest)
- Audit log of every config change (`audit_log` table; every API write writes one row)
- Backup verification (automated restore test weekly)
- Access reviews quarterly (script that emails admins their team's permissions)

### EU data residency

For European clients: deploy to Fly.io `fra` (Frankfurt) or AWS `eu-west-1` (Ireland). Postgres replication across regions.

### Verifier portal

Per-run share link with read-only access for an external auditor — they see the audit view (Phase 2), download XML/PDF, comment on emission lines. No code access, no PII.

---

## Phase 8 — Sales / onboarding tooling (~2 weeks)

### Self-service onboarding wizard

```
Step 1 — Sector + country               [aluminium / fertiliser / steel] × [MZ / ZA / MA / EG]
Step 2 — Facility identity              name, EORI, UN-LOCODE, GPS, capacity
Step 3 — ERP connector picker           [ERPNext / SAP / Oracle / Dynamics / NetSuite / Sage / Odoo]
Step 4 — Cred entry                     fields auto-rendered from ConnectorSpec
Step 5 — Test connection                runs ERPNextClient.ping() (or equivalent)
Step 6 — Initial sync                   triggers background job, shows progress
Step 7 — Review + verify                lands on /dashboard/facilities/<id>
```

Use the existing `ConnectorSpec.credentials` schema to render the cred form auto-magically — same pattern as the manual forms.

### Demo data toggle

For sales: "Show me what this looks like" button → spins up a demo tenant with Mozal data pre-seeded, gives the prospect a read-only token. Self-destructs after 7 days.

### Trial conversion

After 14 days of demo data: prompt to onboard their real ERP. Migration is one connector swap; canonical data structure is identical.

---

## Phase 9 — Defensibility / moat (~ongoing)

What makes this hard to copy in year two:

1. **EF database curation** — the calc engine quality is proportional to the depth of the lookup tables. Build a continuously-curated database of EFs sourced from peer-reviewed papers + verifier reports, tagged with provenance and freshness date.
2. **Supplier portal network effects** — every supplier we onboard for one client makes us better for the next. Build a shared supplier directory (opt-in) with verified embedded-emission declarations.
3. **EU verifier relationships** — partner with 1-2 EU-accredited verifiers (DNV, TÜV, Bureau Veritas) for joint go-to-market. They review our output, sign off, get a referral fee.
4. **Industry-specific seeders** — every new sector profile we ship lowers onboarding time for that sector's next client. Charge a premium for sectors only we cover.
5. **Compliance-as-code** — when CBAM v2 / Singapore / California carbon programs hit, we ship the schema update faster than incumbents.

---

## Build-order summary

| Phase | What | Duration | Status |
|---|---|---|---|
| 1 | Close calc-engine soft spots | 1 week | not started |
| 2 | Web UI / dashboard (Next.js + Tremor) | 3 weeks | not started |
| 3 | PDF report generator | 1 week | not started |
| 4 | FastAPI + Postgres + RQ + observability | 2 weeks | not started |
| 5 | Multi-tenancy + auth + billing | 2 weeks | not started |
| 6 | Steel + hydrogen + cement sectors | 1 week each | not started |
| 7 | SOC 2 prep + EU data residency + verifier portal | ongoing | not started |
| 8 | Onboarding wizard + demo data toggle | 2 weeks | not started |
| 9 | Defensibility / moat | ongoing | not started |

**~8 weeks of focused engineering to a YC-ready product**, parallelisable to ~5 calendar weeks with two engineers (one full-stack on Phase 2–3, one infra on Phase 4–5).

---

## Anti-goals (what NOT to build)

- ❌ A "general-purpose carbon-accounting platform" — stay laser-focused on CBAM
- ❌ Your own ERP — we lean on ERPNext + the connector framework
- ❌ A new visualisation library — use Tremor / shadcn / TanStack
- ❌ Custom auth — Clerk
- ❌ Custom queue — RQ
- ❌ On-prem deployment in v1 — cloud-first, with EU regions for residency
- ❌ Manual sales motions — the demo data toggle does first contact
- ❌ Build for sectors before there's a client — the framework is designed to make sector expansion cheap; do it just-in-time

---

## Open architectural questions

1. **CEMS / SCADA real-time ingest** — when a client has 1-minute meter data, do we stream or batch? Today's MVP is monthly; the calc engine is built around monthly aggregation. Streaming changes the storage assumption.

2. **Reactive recalculation** — when an EF in the lookup table updates (e.g. new IPCC defaults), should past quarters recalculate? Current default: no, runs are immutable. Audit-friendly but creates "as of" complexity.

3. **Per-CN code allocation** — when one Work Order produces N coproducts with different CN codes (CBAM relevant for steel), the current allocation works at the *product* level but the canonical model assumes one CN per Work Order. Steel rollout will need a `ProductionRun.coproduct_cn_codes` field.

4. **Vendor-attested precursor EE refresh** — when a supplier updates their portal-submitted EE for past purchases, do downstream client SEE numbers refresh? Lock to original quarter or apply retroactively?

5. **Multi-currency contracts** — Mozal sells in USD, OCP in EUR, customers pay in EUR. The current FX-to-EUR conversion handles activity costs but not contract-level realised gains/losses. Becomes material at scale.

Document the resolution to each before Phase 5.

---

## What to do tomorrow morning

If you're picking this up fresh:

1. Run **[02_SETUP_AND_RUN.md](02_SETUP_AND_RUN.md) §2 (smoke test)** — confirms calc engine works on your machine in 30 seconds.
2. Run **§3 (full ERPNext path)** — confirms ingestion + seeding works end-to-end.
3. Read **[01_OUTPUTS.md](01_OUTPUTS.md)** with the actual files open — you'll see how the abstractions map to artefacts.
4. Pick **one Phase 1 item** (Stock-Entry ingestion is the highest-leverage) and ship it in a day.
5. Once Phase 1 is done, **clone a Next.js starter, drop Tremor in, and render the dashboard JSON** — you'll have a defensible demo screen by end of week 2.

The data layer is solid. The hard part is shipping the visible surface fast enough that prospects believe the platform is real.
