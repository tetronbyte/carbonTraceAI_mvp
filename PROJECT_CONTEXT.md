# PROJECT_CONTEXT

Handoff file: current state of the project. Stable working rules live in [AGENTS.md](AGENTS.md).

## 1. Overview
carbonTraceAI is an EU CBAM carbon-accounting MVP for African mid- and large-cap manufacturers (aluminium, fertilisers). It ingests ERPNext, manual, supplier and OCR data into a canonical store, runs the CBAM calculation engine, and produces XML, CSV and JSON reports plus a web dashboard.

## 2. Tech stack & how to run
- Backend: Python, FastAPI, SQLAlchemy, SQLite. Local `.venv` is Python 3.14.3.
- Frontend: Next.js 15, React 19, Tailwind, Recharts. `/api/*` is proxied to `:8000` via `frontend/next.config.mjs`.
- ERP sandbox: ERPNext in Docker (`docker-compose.erpnext.yml`, port 8080). Requires Docker Desktop running.
- Run commands: see [AGENTS.md](AGENTS.md). Full walkthrough: [docs/05_FULL_STACK_SETUP.md](docs/05_FULL_STACK_SETUP.md).

## 3. Structure
- `src/api/` FastAPI app and background jobs. `jobs.py` holds the pipeline and the synthetic demo supplements.
- `src/ingestion/`, `src/onboarding/`, `src/seeding/` ERP, manual and OCR ingestion, connectors, ERPNext seeder.
- `src/calculation/` CBAM calc engine and report renderer.
- `src/storage/`, `src/core/` canonical repository and models.
- `frontend/` Next.js UI.
- `scripts/` one-shot CLIs (seed, pipeline, calculation, onboarding, demo launcher). `build_cbam_defaults.py` rebuilds the official defaults CSV from the OJ HTML.
- `data/cbam_default_values_2026_1740.csv` official CBAM default values, all 122 country tables (IR 2025/2621 Annex I as replaced by IR 2026/1740). Loaded by `lookup_tables.cbam_default`.
- `tests/test_zero_emission_fixes.py` regression tests for the 0 tCO2e failure.
- `deploy/` systemd units and nginx config (uncommitted).
- `docs/` handover docs. `reports/`, `research_notes/` market research (uncommitted).
- `.claude/launch.json` dev server configs for the Claude desktop app.

## 4. Current status
As of 2026-11-05, on this Windows machine:
- Works end to end for the Mozal profile: fresh sandbox, seed with `errors=0`, UI run, dashboard, report endpoints. Q3 2026 result: 613,675 tCO2e, SEE 4.914 t/t, projected cost EUR 27.69M. Rerunning gives the same total and row counts.
- 40 tests pass (2026-11-20); `tsc --noEmit` was clean on 2026-11-05 (frontend not touched since).
- Official CBAM default values are wired in (2026-11-20): `lut.cbam_default(cn, iso2, year)` = TOTAL column, longest CN/TARIC prefix, country unmapped or "-" -> Other table, mark-up 10/20/30 % (2026/27/28+), fertilisers 1 %. Precursor defaults use it (supplier country, else facility country). Each product also gets `default_see_tco2_per_t` / `default_cbam_certificate_cost_eur` (also in dashboard JSON as `defaultSEE`, `defaultCbamCostEUR`); the frontend does not show them yet.
- Demo numbers above predate this change and were not rerun.
- **These numbers are demo numbers.** Meter, aluminium process and supplier rows are synthetic, generated in `_emit_demo_manual_supplements`. 72% of emissions are estimated, so the product is flagged.
- Not working or not verified:
  - OCP profile: not run. Facility-level energy and process records are counted in full for each CN, so multi-CN totals are overstated (the engine now warns). `run.facility_reports[0]` and the facility-row match also assume one facility in the store.
  - Reconciliation shows n/a: the engine imports the checks but never calls them.
  - OCR is skipped because Tesseract is not installed.
  - Quality inspections are seeded, but no runner stream pulls them.
  - The data-gaps banner on the dashboard typechecks but has not been seen rendered, since this run has no warnings.
- Working branch is `main`, pushed to `origin/main`. `master_old` and old `master` also on remote.

## 5. Done log
- 2026-11-23: Split branches: `main` (all work, new changes go here) and `master_old` (frozen copy of old `master`).
- 2026-11-20: Wired official CBAM default values (IR 2026/1740) into the calc engine: CSV + builder script, `cbam_default` loader with mark-up and Other-table fallback, precursor defaults, default-method SEE/cost per product, tests (40 pass). Replaced invented `CBAM_DEFAULT_EMBEDDED`.
- 2026-11-05: Started the stack on Windows. Added `.claude/launch.json`, this file and `AGENTS.md`.
- 2026-11-05: Fixed runs reporting 0 tCO2e as success: PO item codes now map to emissions rows, demo energy/process/supplier rows are dated in the reported quarter, setup wizard works, seeder stops hiding errors, Stock Entry, Quality Inspection, Purchase Invoice and Sales Invoice payloads fixed, reruns replace rows, zero-emission runs fail.

## 6. Decisions & rationale
- Branches (2026-11-23): `main` = all work, where every change now goes. `master_old` = `e7c962a`, the old `master` exactly as it was (includes all 2026-11-20 work), kept as a frozen snapshot. Old `master` was renamed. Remote `master` still exists: switch GitHub default to `main`, then delete it. Worktree `cbam-emission-factors-030151` removed; its notes are in `research_notes/`.
- Precursors that are not CBAM goods (alumina, anode, AlF3, phosphate rock, potash, sulphur) get 0 embedded emissions on the default path (no invented values). A supplier-declared actual value for them is still counted; whether to drop that too is open (section 8).
- Default values come from the OJ HTML (legally binding), not the Commission XLS. ISO2 -> OJ country name map in `lookup_tables._EU_COUNTRY_NAME` covers only MVP/target countries.
- A run with output but 0 tCO2e fails rather than publishing a report, because zero means missing inputs.
- A supplier declaration citing a PO number replaces that PO row, so its tonnage is not counted twice.
- Each pipeline run clears the facility's canonical rows first, because rows get new UUIDs on ingest. `ingestion_events` stays append-only.
- Work Orders and Stock Entries stay drafts: submitting needs raw material stock, and no purchase receipts are seeded. Stock Entries keep the Work Order in `custom_work_order`.
- `NAT-GAS-FS` is not mapped as fuel: feedstock gas counts as process CO2 through the fertiliser record.

## 7. Next steps / TODO
1. Decide the CBAM scope question in section 8; it changes the headline cost. Audit details: `research_notes/` in worktree `cbam-emission-factors-030151` (`CBAM_formula_values_audit_2026-11-20.md`).
2. Show actual vs default SEE/cost on the dashboard (`frontend/`), and drop indirect from actual SEE/cost for aluminium, steel, hydrogen.
3. Make the OCP profile correct: split facility-level energy and process across CNs, handle more than one facility.
4. Wire the reconciliation checks into the engine.
5. Review and commit the uncommitted work.
6. Install Tesseract if the OCR path is needed.
7. Product backlog: [docs/06_NEXT_STEPS.md](docs/06_NEXT_STEPS.md).

## 8. Open questions / blockers
- CBAM scope, needs checking against the regulation: the certificate cost uses total SEE (direct + indirect + precursors). As recalled, CBAM counts only direct emissions for aluminium, and alumina may not be a relevant precursor. If so, the cost is overstated. Not changed.
- Non-CBAM precursors with a supplier-declared value are still counted. CBAM counts only relevant precursors that are CBAM goods; drop them entirely? (Tests `test_engine_runs_aluminium_facility` and the pipeline tests rely on alumina being counted.)
- UI wording: "VERIFIED OUTPUT" and "supplier portal declaration (verified)" appear on synthetic demo data.
- Docs say Python 3.12+ and ERPNext `v15.74.4`; the local venv is 3.14.3 and the compose file uses `v15.120.0`.

