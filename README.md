# carbonTraceAI — CBAM Carbon Accounting

Market-ready ingestion + canonical-store + calculation engine for CBAM-compliant
carbon accounting of African mid- and large-cap manufacturers. Produces audit-ready
EU CBAM XML, dashboard-ready CSV/JSON, and PDF (next phase).

> **New here?** Read the handover docs in [`docs/`](docs/):
> - [01 — Outputs](docs/01_OUTPUTS.md) — every artefact the pipeline produces
> - [02 — Setup & Run](docs/02_SETUP_AND_RUN.md) — clean-machine to first report in 6 commands
> - [03 — Roadmap](docs/03_ROADMAP.md) — what's next, in build order

## MVP scope

| Dimension | In scope |
|---|---|
| Regulation | EU CBAM only |
| Sectors    | Aluminium (Mozambique, South Africa), Fertilisers (Morocco, Egypt) |
| ERP        | **ERPNext** (open-source) — local Docker sandbox, ngrok-tunnelable for cloud Airbyte |
| Ingestion  | ERPNext (REST + Airbyte connector), Manual entry, Supplier portal, OCR for invoices |
| Sensors    | Manual entry only — no SCADA/IoT in MVP |

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  ERPNext sandbox (docker-compose.erpnext.yml, frappe/erpnext v15)    │
│  Seeded with a realistic factory profile:                            │
│    • mozal_aluminium  — primary Al smelter, 24 months, ~1.5k records │
│    • ocp_fertiliser   — ammonia/urea/DAP/HNO3, 24 months, ~1.7k recs │
│                                                                      │
│  Auth: API key + secret. Visible at http://localhost:8080            │
│  Remote demo: `ngrok http 8080` exposes a public HTTPS URL           │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                              ▼
       ┌──────────────────┐         ┌────────────────────────────┐
       │  ERPNext REST    │         │  Airbyte ERPNext source    │
       │  (Frappe API)    │         │  (provisioner — when Airbyte│
       │  default path    │         │   is deployed; same auth)  │
       └────────┬─────────┘         └──────────────┬─────────────┘
                │                                  │
                └────────────────┬─────────────────┘
                                 ▼
                ┌──────────────────────────────────────┐
                │  JSONL landing zone                  │
                │  data/raw/erpnext/<stream>/<ts>.jsonl│
                └──────────────────┬───────────────────┘
                                   ▼
                       ┌────────────────────────────┐
                       │ ErpIngestor + mappers      │
                       │ Manual / Supplier / OCR    │
                       └──────────────┬─────────────┘
                                      ▼
                       ┌────────────────────────────┐
                       │ Canonical Pydantic models  │
                       │ Repository (SQLite, 10 tbl)│
                       │ + ingestion_events audit   │
                       └────────────────────────────┘
                                      ▼
                       (downstream: cleaning → calc → CBAM report)
```

## Layout

```
config/                    settings, CBAM data dictionary + grid EFs
src/core/                  Pydantic models, enums, BaseIngestor, exceptions
src/storage/               SQLite repository (canonical store + audit)
src/ingestion/
  erp/
    erpnext_client.py      Frappe REST client (auth, iter_all, insert)
    erpnext_runner.py      Doctype → canonical-stream JSONL writer
    erp_ingestor.py        JSONL → canonical Pydantic models (mappers)
    airbyte_client.py      Airbyte API stub (used by erpnext_airbyte path)
  manual/                  facility / sensor / supplier / fugitive forms
  ocr/                     pdfplumber + Tesseract invoice extraction
  orchestrator.py          one entry point for all four sources
src/onboarding/            connector registry, vault, factory (REST + Airbyte)
src/seeding/               FactoryProfile + ERPNextSeeder
src/utils/                 logger, JSONL landing zone
scripts/                   one-shot CLIs
tests/                     mocked + integration smoke tests
docker-compose.erpnext.yml frappe_docker stack
```

## Quick start

```bash
# 0. Python deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Boot ERPNext (first run takes ~3-5 min for the new-site bootstrap)
docker compose -f docker-compose.erpnext.yml up -d
# Wait until http://localhost:8080 is reachable (Administrator / admin)

# 2. Seed it with a realistic factory dataset (~1.5–2k records)
python -m scripts.seed_erpnext --profile mozal_aluminium
# or --profile ocp_fertiliser

# 3. Run the full ingestion pipeline against the live ERPNext
python -m scripts.run_erpnext_pipeline --facility-id MOZAL-MZ-01

# 4. (Demo to remote stakeholder) Expose ERPNext via ngrok
ngrok http 8080
# Plug the resulting https URL + API key + secret into your onboarding form,
# or pass --base-url to run_erpnext_pipeline.
```

## Six CBAM collection methods

| Code | Implemented in |
|---|---|
| **ERP**      | `src/ingestion/erp/` (REST + Airbyte) — primary path |
| **METER**    | `src/ingestion/manual/sensor_entry.py` — manual entry, no SCADA in MVP |
| **INVOICE**  | `src/ingestion/ocr/` (pdfplumber + Tesseract) |
| **MANUAL**   | `src/ingestion/manual/manual_ingestor.py` |
| **SUPPLIER** | `src/ingestion/manual/manual_ingestor.py` (Block E portal) |
| **CALC**     | downstream calc engine (out of scope here) |

## Onboarding a client connection

The connector registry advertises ERPNext (direct + via Airbyte), SAP S/4HANA,
Oracle EBS, MS Dynamics 365, NetSuite, Sage X3, and Odoo. Pick one in the
onboarding flow, enter creds (Fernet-encrypted at rest), and trigger a sync:

```bash
python -m scripts.onboard_client --list
python -m scripts.onboard_client --connector erpnext_direct --facility-id MOZAL-MZ-01
```

## Calculation engine

`src/calculation/` runs the full CBAM math and emits three artefacts per run:

| Module | What it does |
|---|---|
| `lookup_tables.py` | IPCC NCV / EF / OF defaults, CBAM Annex II/VIII embedded-emission defaults per CN code, AR5 + AR6 GWPs, country grid EFs, FX-to-EUR table, EUA reference price |
| `estimators.py`    | Fills any missing NCV / CC / OF / EE / grid-EF / steam-EF / PFC / N2O with IPCC defaults + the ±uncertainty CBAM IR Art.4(3) allows. Every estimate is tagged with provenance and tier. |
| `ef_priority.py`   | Resolves EF candidates in the order: measured > supplier-actual > national > CBAM-default > IPCC-default > estimated |
| `uncertainty.py`   | RSS combination of relative + additive uncertainty; tracks the share of estimated emissions per product (verifier flag if > 20%) |
| `formulas.py`      | Direct SEE, Indirect SEE, complex-goods SEE, adjusted SEE (carbon-price-paid deduction) |
| `allocation.py`    | Coproduct allocation on mass / energy / economic basis |
| `aggregation.py`   | Monthly → quarterly window resolution + per-(facility, CN) bucketing |
| `reconciliation.py`| Mass-balance, energy-balance, GL cross-check residual checks |
| `carbon_price.py`  | Block G — converts local carbon tax paid to EUR/tCO2e, deducts from SEE |
| `renderer.py`      | EU CBAM IT-Tools XML, flat CSV (dashboard-ready), pre-aggregated dashboard JSON |
| `engine.py`        | Orchestrator: reads canonical Repository → buckets by quarter → runs formulas → rolls up → flags estimation overrun |

Run it:

```bash
python -m scripts.run_calculation 2026-Q2
```

Output goes to `data/reports/`:

```
data/reports/
  cbam_quarterly_<run_id>.xml     # EU CBAM IT-Tools schema
  cbam_quarterly_<run_id>.csv     # one row per (facility × product × quarter)
  dashboard_<run_id>.json         # pre-aggregated totals + per-line breakdowns
```

## Sample output (Mozal Q2 2026)

```
CBAM run 88927752-38ab-4ffe-8bbb-0c769e51ed50
  • MOZAL-MZ-01 [2026-Q2]  total=204,207 tCO2e  CBAM cost=€6,738,840  flagged_products=1
      ↳ CN 76011000  out=50,000t  SEE=4.084  adj=2.995  ±4.5%  est-share=36.3%
```

— total emissions, projected CBAM certificate cost in EUR, adjusted SEE after
the country-of-origin carbon-tax deduction, propagated uncertainty, and the
share-of-estimated-emissions flag (>20% triggers a verifier warning per
CBAM IR Art.4(3)).

## Extending downstream

- **Cleaning** — add `src/cleaning/` (dedup, FK validation, unit normalisation) before the calc engine if the data quality demands it
- **Live FX & EUA spot** — replace the static `lookup_tables.FX_TO_EUR` and `EUA_PRICE_EUR_PER_TCO2E` with an ECB / ICE feed
- **Dashboard UI** — point any front-end at `data/reports/dashboard_<run_id>.json`

The canonical model and the calc engine's `CalculationRun` are the contract — keep them stable.

## Removed in the 2026-05 architecture pivot

The earlier DataGen synthetic-stream simulator and its config schemas have been
removed. Every ingestion path now flows through a real ERP system of record
(ERPNext for the demo; SAP / Oracle / Dynamics / NetSuite / Sage / Odoo for live
clients via the same connector framework).
