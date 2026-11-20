# carbonTraceAI — Idea Document

## 1. Idea

CBAM (EU Carbon Border Adjustment Mechanism) compliance SaaS for African mid/large-cap manufacturers exporting to EU. Pulls production/procurement data straight from customer's ERP, runs full CBAM carbon-accounting math (IPCC + EU Annex defaults, uncertainty, allocation), outputs audit-ready XML for EU CBAM portal + dashboard for the company + PDF for CFO/verifier.

Problem: CBAM definitive regime starts 2026. Exporters must report embedded emissions per shipment or face certificate costs. Most African manufacturers have no carbon-accounting system, no EU compliance tooling, and CBAM math (SEE formulas, EF priority tiers, uncertainty propagation, coproduct allocation) is complex, spreadsheet-hostile, and audit-grade traceability is manual/expensive today (consultants, spreadsheets).

Wedge: ERP-native ingestion (not manual data entry) + verifier-grade provenance (every number traces back to source ERP record) + Africa-specific sector defaults (aluminium, fertiliser first).

## 2. Core Features

- **ERP ingestion**: ERPNext live (REST + Airbyte), extensible connector framework advertising SAP, Oracle EBS, Dynamics 365, NetSuite, Sage X3, Odoo. 4 more collection paths: manual entry, supplier portal, OCR (invoices via pdfplumber+Tesseract).
- **Canonical data layer**: 20-table Pydantic/SQLite store, full audit trail (`ingestion_events`, `raw_ref` back-pointers to source JSONL → ERP document).
- **CBAM calculation engine**: IPCC/EU Annex VIII lookup tables, EF resolution priority (measured > supplier-actual > national > CBAM-default > IPCC-default > estimated), uncertainty propagation (RSS), coproduct allocation (mass/energy/economic), carbon-price-paid deduction, mass/energy/finance reconciliation checks, estimation-share verifier flag (>20% per CBAM IR Art.4(3)).
- **Outputs**: EU CBAM IT-Tools XML (declarant upload), flat CSV (BI-ready), pre-aggregated dashboard JSON, PDF report (planned).
- **Dashboard/UI**: Next.js + Tremor — KPI tiles, emissions breakdown donut, per-product SEE bars, reconciliation health, per-line provenance table, audit view for verifiers (click any number → source ERP record).
- **Onboarding**: connector picker + credential vault (Fernet-encrypted), self-service wizard planned.

## 3. Business Model

- **B2B SaaS, usage-based**: per facility × quarter, or per CBAM certificate value tracked.
- Tiering sketch (from roadmap): Free (1 facility, capped records, no PDF export) → Growth (~€499/facility/month, unlimited, XML+PDF export) → Enterprise (custom, multi-region, SSO, dedicated CSM).
- **Target customer**: African mid/large-cap manufacturers in CBAM sectors (aluminium, fertiliser, steel, cement) exporting to EU — direct-sell or via EU-accredited verifier partnerships (DNV, TÜV, Bureau Veritas) as referral channel.
- **Moat plan**: curated EF database (provenance + freshness), supplier-portal network effects (shared verified-EE directory), verifier relationships, sector-specific seeders (each new sector lowers next client's onboarding cost), compliance-as-code (fast to adapt when CBAM v2 / other carbon border regimes land).

## 4. Tech Stack

| Layer | Current | Planned |
|---|---|---|
| ERP sandbox | ERPNext (Frappe, Docker) | — |
| Ingestion | Python — REST client, Airbyte stub, OCR (pdfplumber/Tesseract) | live FX/EUA feeds (ECB/ICE) |
| Storage | SQLite, 20-table canonical Pydantic store | Postgres + Alembic + RLS multi-tenant |
| Calc engine | Python, pure functions (formulas/allocation/uncertainty/reconciliation) | GL/stock-movement reconciliation wiring |
| API | FastAPI (`src/api/main.py`) exists | full route set, auth middleware |
| Frontend | Next.js + Tremor/shadcn dashboard exists (per docs 04-06) | Sankey diagrams, multi-facility switcher, facility map (Mapbox/MapLibre) |
| Auth | none yet | Clerk (or Supabase Auth) |
| Jobs | synchronous scripts | RQ/Celery + Redis |
| PDF | not built | WeasyPrint (HTML→PDF, reuse dashboard templates) |
| Billing | none | Stripe usage-based |
| Deploy | local Docker | Vercel (frontend) + Fly.io (API/Postgres), EU region for residency |
| Observability | none | Sentry, OpenTelemetry, structlog |

## 5. Validation

**What's proven (working code, not just design):**
- Full pipeline runs end-to-end on seeded realistic data: ERPNext → ingestion → canonical store → calc engine → 3 output artefacts. ~5,000 ERPNext records, ~4,000 JSONL rows, ~5,000 canonical rows per demo run.
- Sample verified output: Mozal Q2 2026 — 204,207 tCO2e, CBAM cost €6.74M, SEE 4.084 (adjusted 2.995), ±4.5% uncertainty, 36.3% estimated flagged correctly.
- 30 passing smoke/integration tests.
- CBAM XML populated against IR 2023/1773 Section 1/2/3/5/6/7/8/9 tags.

**What's NOT yet validated:**
- No real customer/pilot — all data is a stoichiometrically-coherent *simulated* factory (Mozal aluminium, OCP fertiliser), not live customer ERP data.
- No verifier (DNV/TÜV/etc.) has reviewed or signed off on output.
- No paying customer, no LOI, no market pricing test — business model tiers are proposed, unvalidated.
- Official CBAM XSD not yet published by EU Commission — XML shape not schema-validated against final spec.
- No auth/multi-tenancy — not production/security ready for a real customer's data.
- Steel/cement/hydrogen sectors (larger CBAM cost exposure per roadmap) not built — only aluminium + fertiliser.

**Next validation steps** (from own roadmap): get 1 real pilot on real ERP data, get 1 verifier partner to review a report, get first LOI/paying customer.

## 6. Strengths & Weaknesses

### Strengths
- Real, working, non-trivial calc engine — not a mockup. Handles the actually-hard parts (EF priority resolution, uncertainty propagation, coproduct allocation, carbon-price deduction) that most "CBAM calculators" skip.
- ERP-native ingestion is the right wedge — customers already have the data in their ERP; manual entry tools (competitors) don't scale to audit-grade traceability.
- Verifier-grade provenance (`raw_ref` chain from output number → JSONL → ERP doc) is a genuine differentiator for an audited compliance product — trust is the product.
- Sector/country framework is generically extensible (new sector = profile + defaults + engine branch), lowering marginal cost of expansion — good for a services-to-product moat.
- Clear, realistic build roadmap already written (this team knows its own gaps).

### Weaknesses
- Zero real customers/pilots — entire validation is self-generated simulated data. Market pull unconfirmed.
- No auth, no multi-tenancy, no billing — not sellable as SaaS today, needs ~4-8 weeks infra work before first paying customer.
- Narrow sector coverage (Al + fertiliser) vs. much larger CBAM cost exposure in steel/cement — competitors could out-cover on sectors.
- CBAM itself is regulatory-dependent: timeline slips, scope changes, or XSD delays are outside the company's control and stall go-to-market.
- Small addressable market if scoped only to "African CBAM exporters" — will likely need geo/regulation expansion (other carbon border regimes) to reach venture scale.
- Heavy reliance on ERPNext-specific integration depth today; other ERP connectors (SAP, Oracle) are stubs/registry entries, not built — real enterprise customers often run SAP, which is unproven here.
- No verifier partnership yet — credibility with EU auditors, who ultimately gate customer trust, is unestablished.
