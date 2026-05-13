# 06 — Next Steps: Hardening, Polish, Scale

Where the full-stack build is, what's still soft, and the build order to get to
a defensible commercial product. Supersedes the calc-engine-only roadmap in
[03_ROADMAP.md](03_ROADMAP.md) — read this for current-state priorities.

---

## Is the frontend end-to-end complete?

**Functionally yes — every desired output is rendered.** Honestly, no — there
are seven specific UX gaps that would matter for a YC pitch in front of an
informed audience. Splitting it by question:

### Does it give all desired outputs in the best possible way?

| Desired output (from the brief) | UI surface | Status |
|---|---|---|
| Factory profile selection | landing `/` — 2 cards | ✅ complete |
| ERP sample admin creds login | landing right panel | ✅ complete |
| ERP pull happens | `/runs/[id]/progress` step rows | ✅ complete + streaming log |
| Calc engine output (CBAM cost, SEE) | `/runs/[id]` KPI tiles + charts | ✅ complete |
| Downloadable reports | `/runs/[id]/reports` — XML / CSV / JSON | ✅ complete |
| Dashboards / visualisation | `/runs/[id]` — donut + bars + tables | ✅ complete, but no Sankey yet |
| Final CBAM audit report | XML download + `/runs/[id]/audit` view | ✅ complete |
| **Convey depth of ingestion pipeline** | `/runs/[id]/audit` "depth banner" | ✅ complete — 5-source tiles + 20-table volumes |
| **Verifier-grade per-line provenance** | audit page line cards | ✅ complete — tier + EF source on every line |
| Reconciliation residuals | dashboard reconciliation card | ✅ complete (finance pending GL ingestion wiring) |
| `raw_ref` drill-down | API endpoint exists; no click-through in UI | 🟡 partial — backend ready, UI not wired |

So: **all 10 of the "what the verifier sees" + "what the dashboard sees" items from your brief are visible in the UI**, with one click-through partially wired (`raw_ref` deep-link). The remaining gaps are polish.

### The 7 soft spots that would matter for a YC pitch

| # | Gap | Why it matters | Effort |
|---|---|---|---|
| 1 | **No Sankey diagram** | The story "alumina + anode + electricity → primary Al → 30 kt to EU" is visually clearer than a donut. Verifiers and partners get it instantly. | 1 day — `d3-sankey` + custom React |
| 2 | **No multi-facility switcher** | Dashboard renders `facilities[0]`. When the demo has both Mozal + OCP in the store, the second is invisible. | 2 hours |
| 3 | **`raw_ref` drill-down UI** | API works (`/api/runs/{id}/raw-ref`); audit-page emission lines don't yet open a modal showing the source JSONL row. The credibility unlock for verifiers. | 3 hours |
| 4 | **No PDF report** | XML + CSV + JSON cover audit + BI. A board-pack PDF closes the "I want to email this to my CFO" loop. | 1 day — WeasyPrint server-side |
| 5 | **No auth** | Anyone with the URL can hit `/api/runs` and trigger a pipeline. Fine for `localhost`; not OK over ngrok. | 4 hours — FastAPI `HTTPBasic` or Clerk drop-in |
| 6 | **Polling not SSE** | 800 ms poll is fine for the 30-second pipeline. Looks less premium than a live tail. | 2 hours — `sse-starlette` is already in requirements |
| 7 | **No facility-map view** | A world map with the four MVP facilities and their grid-EF heat is high-impact in pitch decks. Tells the Mozambique-hydro-advantage story instantly. | 1 day — MapLibre + topojson |

**Recommended order**: 3 → 1 → 2 → 4 → 5 → 6 → 7. The first three are the audit-credibility ones; 4–5 unblock external pitching; 6–7 are pure polish.

---

## Is the calc engine perfect / can it be made more robust?

It's comprehensive — see [04_FRONTEND_AND_API.md "8 honest gaps"](04_FRONTEND_AND_API.md). Six are closed; two are deferred (XSD validation, steel/hydrogen). Beyond those, the next dials of robustness:

### Calc-engine robustness — Phase A (~1 week)

| Item | What | Why |
|---|---|---|
| **Sampling-frequency → uncertainty curve** | Right now `MonitoringMeta.uncertainty_pct` is a free number. Make it derive from sampling frequency: continuous = 2.5%, daily = 5%, monthly = 10%, annual = 20%. | Verifier explicitness |
| **GL-driven finance reconciliation** | `gl_entries` ingestion mapper landed in this build; the calc engine doesn't yet read them. Sum debits to fuel accounts, compare to PO costs, report residual. | Closes the third reconciliation leg |
| **Stock-movement mass balance** | Same — `stock_movements` ingest but engine doesn't yet use them to compare `Σ goods-issue qty ≈ Σ BOM-line × WO output`. | Tightens the mass-balance check from BOM theory to actual movement |
| **EUA live feed** | Path is wired (env override + Frankfurter FX). Add a paid ICE / Refinitiv feed for live EUA spot. | Real-time CBAM cost projection |
| **Lookup-table expansion** | `CBAM_DEFAULT_EMBEDDED` has 12 CN codes; official Annex VIII has ~50. Bulk-load the Commission CSV. | Audit coverage |
| **AR5/AR6 GWP set switching** | Both are loaded; the engine picks AR6. Make this per-tenant configurable so legacy frameworks that mandate AR5 still work. | Multi-region deployment |
| **Stoichiometric driver tightening** | Seeder ±5 % noise; tighten to ±2 % and assert month-over-month mass balance holds within tolerance. | Validation gold standard |
| **Algorithmic allocation choices** | `coproduct_method` is config-driven, but the engine doesn't yet *justify* the choice in the XML output. Add a one-line explainer per product. | Verifier sign-off |

### Calc-engine robustness — Phase B (~2 weeks)

| Item | What | Why |
|---|---|---|
| **Steel sector branch** | CN 7201–7301, BFG/BOF gas, coke reductant vs combustion split, pig iron/DRI/scrap precursors, limestone calcination | Tier-1 client volume — South32, ArcelorMittal SA |
| **Cement sector** | CN 2523, clinker calcination + alternative fuels | Morocco / Egypt expansion |
| **Hydrogen sector** | CN 28041000, SMR / ATR / electrolysis pathways, CCS credit | Future-facing demand |
| **CEMS high-frequency ingest** | `MeterType.STACK_N2O` and `SamplingFrequency.CONTINUOUS` exist; streaming ingest path doesn't. | Tier 3 audit credential |
| **Verification opinion modelling** | `VerificationOpinion` enum exists; populate from a workflow (Pending → Reviewing → Reasonable/Limited/Qualified). | Full audit lifecycle |

---

## Is this a high-level ERP replication of a factory at scale?

It's **shape-faithful at scale** — 8/8 simulator-fidelity gaps closed. Honest improvements still possible:

### ERP fidelity — what's still soft

| Item | What | Why | Effort |
|---|---|---|---|
| **Batch / lot management** | Real factories assign batch IDs to every WO and trace material lots through Stock Entries. We only stamp `batch_run_id` on `ProductionRun`; the link from a batch to its inputs is implicit (via BOM, not via stamped lot). | Verifiers ask "show me the alumina lot that went into this Al ingot batch" | 2 days |
| **Preventive Maintenance module** | ERPNext has `Asset` + `Maintenance Schedule` doctypes. We seed neither. Real factories tie PM windows to production planning (the Aug shutdown for Mozal is hand-coded). | Realistic downtime patterns; PM-driven emissions (cleaning solvents, kiln cool-down) | 1 week |
| **HR / shift roster** | Work Orders use `Administrator` as `shift_supervisor`. Real factories have 3 shifts × 7 days. | Audit log granularity | 3 days |
| **Multi-plant per company** | One Company per profile today. Real Mozal has 4 potlines + 1 casthouse + 1 anode plant. Cost centres exist but aren't tied to physical sub-plants. | Sub-process attribution | 1 week |
| **Vendor compliance metadata** | Each Supplier has country + group. Real Mozal stores: ESG self-disclosure status, last verification date, scrap recycled %, freight emission factor. | Block E credibility | 3 days |
| **Currency drift over time** | Static FX-to-EUR per pull. Real procurement contracts lock prices at quarter boundaries and revalue. | Finance reconciliation accuracy | 2 days |
| **Logistics layer** | Sales Invoice → outbound shipment is now mapped. Inbound logistics (supplier → factory, Scope 3 Cat 4) is unmodelled. | Full Scope 3 picture | 4 days |
| **Year-over-year history** | Seeder emits 24 months at a time. Real factories want 3–5 years for trending. Trivial parameter bump but no UI to view trends. | Trend analytics | 1 week (with UI) |

### Industry-grade simulator depth

If the demo evolves toward "a YC partner's industry expert technical-due-diligences us":

1. **Plant-specific physical model**: per-tenant editable BOM ratios (e.g. a customer running a less-efficient potline has 1.95 t alumina/t Al, not 1.925)
2. **Outage events**: emit "Maintenance Order" doctypes with their own emission cost (cleaning solvents, kiln re-light)
3. **Quality-of-input variation**: alumina from Alunorte vs. Worsley has different impurity profiles → different fluoride consumption → different emissions
4. **Realistic price elasticity**: NG price has monthly correlation, not log-normal random walk
5. **Realistic supplier mix shifts**: a customer switching from Sasol gas to Sonatrach LNG creates a step change

None of these block the YC demo. All matter if a customer's plant engineer reviews the model.

---

## Productionisation — gaps still ahead

### From SQLite to Postgres (~3 days)

```bash
pip install psycopg[binary]
export CARBONTRACE_DB_URL="postgresql+psycopg://carbontrace:****@db/carbontrace"
```

SQLAlchemy handles the switch. Then:

1. `alembic init alembic && alembic revision --autogenerate -m init`
2. Add `tenant_id` UUID column to every table
3. Enable Postgres Row-Level Security (RLS) — per-tenant filter via session GUC
4. Index hot columns: `(tenant_id, facility_id, period_start)`

### Auth (~4 hours for HTTP Basic, ~1 day for Clerk)

**Quick path** — HTTP Basic with a single password:

```python
# src/api/main.py
from fastapi.security import HTTPBasic, HTTPBasicCredentials
security = HTTPBasic()

@app.middleware("http")
async def require_auth(req, call_next):
    if req.url.path.startswith("/api"):
        creds: HTTPBasicCredentials = await security(req)
        if creds.password != os.getenv("CARBONTRACE_API_PASSWORD"):
            return JSONResponse(401, {"detail": "unauthorized"})
    return await call_next(req)
```

**Production path** — Clerk:

```bash
cd frontend && npm install @clerk/nextjs
```

Then drop `<ClerkProvider>` in `app/layout.tsx`. Middleware validates JWT, resolves `tenant_id`, sets Postgres GUC.

### Multi-tenancy (~1 week)

- Per-tenant Fernet vault keys (rotate quarterly)
- Per-tenant connector_id namespace
- Per-tenant ERPNext sandbox (each customer gets their own Docker stack, or share + RLS)
- Stripe customer-portal integration (per-facility-per-quarter pricing)

### Observability (~2 days)

```bash
pip install sentry-sdk[fastapi]
cd frontend && npm install @sentry/nextjs
```

- Sentry for errors (frontend + backend)
- OpenTelemetry traces (FastAPI middleware)
- Structured logs (`structlog`) to stdout — Fly.io / Vercel capture
- Custom dashboard panels: pipeline duration histogram, EF tier distribution, share-estimated trend

### CI/CD (~1 day)

`.github/workflows/ci.yml`:

- backend: `ruff check`, `mypy`, `pytest -q`
- frontend: `npm run lint`, `npx tsc --noEmit`, `npm run build`
- preview-deploy to Fly.io / Vercel on PR
- prod deploy on `main` merge

---

## Sector + geo expansion

| Where | Sectors | Effort per |
|---|---|---|
| Mozambique | aluminium (Mozal), heavy mineral sands | done + 3 days for sands |
| South Africa | aluminium (Hillside), steel (Highveld, ArcelorMittal), cement (PPC, AfriSam) | 1 week each |
| Morocco | fertiliser (OCP) | done |
| Egypt | fertiliser (Abu Qir, EBIC), aluminium (Egyptalum) | 2 days each |
| Tanzania | cement (Twiga, Tanga, Heidelberg) | 4 days |
| Nigeria | cement (Dangote, Lafarge), fertiliser (Indorama, Notore) | 1 week |

The framework is designed to make sector + country additions cheap: add `FactoryProfile` → bulk-load CBAM defaults → add engine branch → done. The ERPNext seeder, the runner, the canonical store, and the calc engine are all sector-aware via the same `Sector` enum.

---

## Defensibility / moat

### Year 1 (now → +6 months)

| Investment | Why it's a moat |
|---|---|
| **EF database curation** | The calc engine quality is proportional to the depth of the lookup tables. Maintain a continuously-updated database of EFs sourced from peer-reviewed papers + verifier reports, tagged with provenance and freshness date. |
| **Supplier portal network effects** | Every supplier we onboard for one client makes us better for the next. Build a shared supplier directory (opt-in) with verified embedded-emission declarations. |
| **EU verifier partnerships** | Partner with DNV / TÜV Süd / Bureau Veritas / SGS for joint go-to-market. Their analysts sign off on our outputs; we get referral flow. |

### Year 2 (defining the market)

| Investment | Why it's a moat |
|---|---|
| **Industry-specific seeders** | Every new sector profile lowers onboarding time for that sector's next client. Charge a premium for sectors only we cover (e.g. polysilicon, lithium hydroxide) before CBAM expands. |
| **Compliance-as-code** | When CBAM v2 / Singapore CTax / California carbon program hit, ship the schema update faster than incumbents. Our IPCC + CBAM lookup tables are versioned; calc engine reads via `gwp_set` flag. |
| **Africa-specific data assets** | Build a curated database of African manufacturer EFs (Eskom monthly grid EF, ONEE quarterly disclosure, EDM hydro spillage, SARS carbon-tax-paid registry). |

---

## Build order — focused build plan

If a single engineer is taking this over, here's the sequence I'd run for the
**next 8 weeks**:

| Week | Track | Output |
|---|---|---|
| 1 | Calc-engine Phase A: GL reconciliation + Stock-movement mass balance + EUA live feed | Verifier flag count drops by ~30 % |
| 2 | Frontend: Sankey + multi-facility switcher + `raw_ref` drill-down | Pitch deck demo flows end-to-end with no caveats |
| 3 | Auth + multi-tenant + Postgres migration | First two pilot customers can share an instance |
| 4 | PDF report generator (WeasyPrint, 3 styles) | Board-pack deliverable for CFOs |
| 5 | Steel sector branch + Hillside profile | South32 demo |
| 6 | Onboarding wizard + demo-data toggle | Self-service free trials live |
| 7 | Observability + CI/CD + Fly.io prod deploy | Status-page live; uptime metric |
| 8 | Verifier portal (read-only share links for DNV/TÜV) | Partner integration |

After 8 weeks: 4 pilot customers, 2 verifier partners, ~€100k ARR. After 12 weeks: pricing model validated, first paying mid-cap aluminium customer, foundation for a YC application or a seed round.

---

## Anti-goals (what NOT to build)

- ❌ "General-purpose carbon accounting" — stay laser-focused on CBAM and adjacent African mandates
- ❌ Your own ERP — we lean on ERPNext + the connector framework
- ❌ A new visualisation library — Recharts is enough; Tremor/Visx if charts evolve
- ❌ Custom auth — Clerk or Supabase Auth
- ❌ Custom queue — Redis + RQ when polling stops being enough
- ❌ On-prem deployment in v1 — cloud-first with EU regions for residency
- ❌ Manual sales motions — the demo-data toggle does first contact

---

## Open architectural questions (carry forward)

1. **CEMS streaming ingest** — when a client has 1-minute meter data, do we stream or batch? Today's pipeline is monthly; the calc engine aggregates monthly. Streaming changes the storage assumption.
2. **Reactive recalculation** — when an EF in the lookup table updates (new IPCC defaults, new CBAM Annex), should past quarters recalculate? Current default: runs are immutable. Audit-friendly but creates "as of" complexity.
3. **Per-CN coproduct allocation** — when one Work Order produces N coproducts with different CN codes (CBAM-relevant for steel), the current allocation works at the *product* level but the canonical model assumes one CN per Work Order. Steel rollout will need `ProductionRun.coproduct_cn_codes`.
4. **Vendor-attested precursor EE refresh** — when a supplier updates their portal-submitted EE for past purchases, do downstream client SEE numbers refresh? Lock to original quarter or apply retroactively?
5. **Multi-currency contracts** — Mozal sells in USD, OCP in EUR, customers pay in EUR. The current FX-to-EUR conversion handles activity costs but not contract-level realised gains/losses. Becomes material at scale.

Document the resolution before Week 3.

---

## What to do tomorrow morning

If you've just been handed this codebase:

1. Run **[05_FULL_STACK_SETUP.md §11 (5-command cheatsheet)](05_FULL_STACK_SETUP.md)** — proves the system runs end-to-end on your machine.
2. Open the UI, click through Mozal Q2 → Dashboard → Audit → Reports. **Read every number on every screen.** Get the calc-engine math in your head.
3. Read **[01_OUTPUTS.md](01_OUTPUTS.md)** with the actual files open — see how the abstractions map to artefacts.
4. Pick **one Phase A item** (GL-driven finance reconciliation is the most credible audit story) and ship it in a day.
5. By end of Week 1, the Sankey + multi-facility switcher + `raw_ref` drill-down should land — that's the unblocker for external pitching.

The data layer is solid. The calc engine is comprehensive. The frontend is
demo-credible. The remaining work is polish, hardening, and selling.
