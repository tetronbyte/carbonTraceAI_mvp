# PROJECT_CONTEXT (worktree `cbam-emission-factors-030151`)

Handoff for this worktree. The full MVP and its main handoff file live in the main checkout
(`C:/Users/adire/Documents/carbonTraceAI_mvp/PROJECT_CONTEXT.md`, branch `main`, uncommitted). This branch
(`claude/cbam-emission-factors-030151`, from `master`) holds only the initial commit plus the files below.
General project docs: `C:/Users/adire/Documents/carbonTraceAI_general/` (project rules + CBAM PDF).
Official CBAM legal/guidance library: `carbonTraceAI_general/CBAM/` (index: `CBAM_REFERENCE_LINKS.txt`). Use it as the source of truth for rules and values.
ISSB/IFRS S2 Tanzania library: `carbonTraceAI_general/ISSB_Tanzania/` (index: `ISSB_TZ_REFERENCE_LINKS.txt`).

## 1. Overview
carbonTraceAI: EU CBAM carbon-accounting MVP for African manufacturers. Focus now: Tanzania exports in cement,
fertilisers, iron & steel, aluminium, hydrogen, per `CBAM_Emission_Factors_Tanzania.pdf`.

## 2. Tech stack & how to run
See main checkout `AGENTS.md`. From this worktree, `.claude/launch.json` starts the main checkout's servers:
`api` (uvicorn :8000) and `web` (Next.js :3000) via PowerShell `Set-Location` wrappers.

## 3. Structure
- `research_notes/CBAM_formula_values_audit_2026-11-20.md` audit of MVP formula + values, PDF check, real company data.
- `research_notes/cbam_defaults_2026_1740_TZ_and_other.csv` official default values (TZ + Other countries) from OJ 2026/1740.
- `.claude/launch.json` dev-server configs pointing at the main checkout.

## 4. Current status
- MVP does not implement the CBAM default-value formula (no mark-up, indirect counted for Al/steel/H2, unofficial default values). Details in the audit note.
- PDF values verified against the OJ: all correct except hydrogen (official TZ fallback = 17.740, PDF says 10.820).
- No code changed.

## 5. Done log
- 2026-11-20: ISSB-for-Tanzania library built at `carbonTraceAI_general/ISSB_Tanzania/` (72 files, ~73 MB, 11 folders): NBAA TP 1/2024 (+ TP 1/2018 PIE definition, roadmap, TP 1/2026 both versions, TFRS 1, quarterly updates), BoT 2025 climate + sustainability guidelines for banks, DSE Rules 2022, IFRS S1/S2 full text (official HTML, incl. Dec 2025 GHG amendments), IFRS Tanzania profile, ISSB educational material, industry guidance drafts, GHG Protocol, TCFD, ISSA 5000, Twiga/Tanga/CRDB reports. Index: `ISSB_Tanzania/ISSB_TZ_REFERENCE_LINKS.txt`. Six NBAA PDFs are 404 on nbaa.go.tz; saved from Internet Archive copies.
- 2026-11-20: Official CBAM document library built at `carbonTraceAI_general/CBAM/` (147 files, ~283 MB, 12 numbered folders): all acts based on Reg 2023/956 (found via EU Publications Office SPARQL), consolidated texts, default values (IR 2025/2621 + correction 2026/1740, PDF + HTML), benchmarks (2025/2620, ETS 2026/1412), ETS-linked acts (MRR, AVR, FAR, Dir 2003/87, 2023/959), proposals, Guidance 1-5f, Q&A, factsheets, Excel DVs/benchmarks/communication template, registry manuals, news/price pages. Index with link + description per file: `CBAM/CBAM_REFERENCE_LINKS.txt`. Certificate prices 2026: Q1 75.36, Q2 75.28, Q3 82.32 EUR.
- 2026-11-20: MVP inventory + factor validity + ISSB check: `research_notes/MVP_inventory_values_ISSB_2026-11-20.md`. IPCC fuel factors and AR5 GWPs correct; 21 issues found (AR6 default, non-CBAM gases, no free-allocation adjustment, wrong PFC C2F6 slope, obsolete quarterly XML, etc.). No ISSB/IFRS S2 support at all; TZ NBAA mandates IFRS S1/S2 for PIEs from 2025, TP 1/2026 effective 2027.
- 2026-11-20: Target manufacturer list (TZ + East Africa, all 5 sectors, size class + CBAM scope) written to general folder: `carbonTraceAI_general/CBAM_Target_Manufacturers_Tanzania_EastAfrica.md`. Corrected: Tanga Cement is Scancem/Heidelberg-controlled; Amsons owns Mbeya Cement + Bamburi.
- 2026-11-20: Tanzanian SME research: `research_notes/tz_sme_real_data_2026-11-20.{md,csv}`. Only Twiga + Tanga publish emissions (Twiga 2025: scope 1 923 kt / 506 kg/t, scope 2 32 kg/t, TZ grid EF 0.336 kg/kWh). No SME steel/fertiliser/hydrogen data public; validation rows from EG/IN/global added.
- 2026-11-20: Audited formula + default values; extracted official tables from EUR-Lex; researched public company emissions data; started API + web servers.

## 6. Decisions & rationale
- Official values taken from the OJ HTML (legally binding), not the Commission XLS (informative only).
- Company sustainability-report figures are kept as seed/sanity data only; they are not CBAM-boundary SEE.
- EU acts fetched from Cellar (`publications.europa.eu/resource/celex/<CELEX>`, Accept `application/pdf;type=pdfa2a` for post-Oct-2023 OJ acts); EUR-Lex itself blocks curl (WAF). Corrigenda to CBAM acts have no English version (they fix other languages only).
- Certificate cost should use the official quarterly CBAM certificate price (IR 2025/2548; weekly from 2027), not a static EUA.

## 7. Next steps / TODO
0. DONE 2026-11-20 on the main checkout (see its PROJECT_CONTEXT.md). Original plan kept for reference:
   wire official CBAM default values into the MVP (main checkout `src/calculation/`). Plan:
   a. Copy `scripts/build_cbam_defaults.py` (this worktree, untested) to the MVP; run it on
      `carbonTraceAI_general/CBAM/03_Default_Values_and_Benchmarks/IR_2026-1740_..._Annex_I_and_IV.html` -> `data/cbam_default_values_2026_1740.csv` (all countries; MVP demo plants are MZ and MA, so the TZ+Other CSV is not enough). Spot-check against `research_notes/cbam_defaults_2026_1740_TZ_and_other.csv` (e.g. MZ 7601 = 3.198, TZ 2523 29 00 = 0.900).
   b. Country names in the CSV are EU names; need ISO2 mapping (no pycountry installed): small dict in the loader for names actually present.
   c. `lookup_tables.py`: replace invented `CBAM_DEFAULT_EMBEDDED` with a loader + `cbam_default(cn, iso2, year)`: longest-prefix CN/TARIC match; country missing or "-" -> "Other countries and territories"; use the TOTAL column only (recital 10: direct/indirect are informative); mark-up 10/20/30 % (2026/2027/2028+) for cement, iron & steel, aluminium, hydrogen, 1 % for fertilisers.
   d. `estimators.estimate_precursor_ee`: use it (needs facility country + year); source string "IR 2025/2621 Annex I as replaced by IR 2026/1740". Non-CBAM precursors (alumina, anode, AlF3, phosphate rock, potash, sulphur) have no official default: decide whether to drop them (CBAM counts only relevant precursors that are CBAM goods).
   e. `engine._compute_product`: add default-value SEE + cost per product next to the actual-method result (new fields on `ProductEmissions`), so the dashboard can show actual vs default.
   f. Update tests (`tests/test_calculation.py`, `test_pipeline.py`) and add one for fallback + mark-up.
1. Implement the default-value path with mark-up and per-sector indirect rule (fixes 1-4 in the audit note).
2. Load the CSV into the lookup table with a regulation-version field.
3. Fix hydrogen value in the PDF.
4. Decide whether to buy CDP / GCCA GNR data (quote needed) or pilot with a TZ cement producer.
5. Replace the Mozal demo profile (smelter idle since 2026-03-15) with a Twiga-like cement profile and a scrap-rebar SME profile (Kamal-like); add TZ grid EF 0.336.
6. Real SME data needs operator access: pilot "default vs actual" assessment with a TZ steel or cement SME.

## 8. Open questions / blockers
- Where should this work land: main checkout branch `main` or this worktree branch (which lacks the MVP code)?
- Paid data budget.
