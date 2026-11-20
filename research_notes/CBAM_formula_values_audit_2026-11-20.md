# CBAM formula + default-value audit, real company data (2026-11-20)

Source doc under review: `carbonTraceAI_general/CBAM_Emission_Factors_Tanzania.pdf`.
Official values pulled directly from the OJ text of Implementing Regulation (EU) 2026/1740
(https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601740) on 2026-11-20.
Full Tanzania + "Other Countries and Territories" tables: [cbam_defaults_2026_1740_TZ_and_other.csv](cbam_defaults_2026_1740_TZ_and_other.csv)
(344 rows, decimal comma as in the OJ).

Code audited: main checkout `carbonTraceAI_mvp/` on branch `main` (uncommitted state as of 2026-11-20).
This worktree branch has only the initial commit, so paths below refer to the main checkout.

## 1. Does the MVP follow the formula?

Formula (doc = Reg. 2026/1740 Annex I intro):
`Emissions = Σ qty × TOTAL default × (1 + mark-up)`; TOTAL = direct + indirect, indirect only for cement + fertilisers;
mark-up 10 % (2026) / 20 % (2027) / 30 % (2028+) for cement, steel, aluminium, hydrogen; 1 % for fertilisers.

**No.** Findings in `src/calculation/`:

| # | Finding | Where | Impact |
|---|---|---|---|
| F1 | No default-value path for the final good. Engine only computes actual (bottom-up) emissions: fuel + process + electricity + precursors. `qty × default total` is never computed for the exported good. | `engine.py` ~L195-260 | Doc formula not implemented |
| F2 | No mark-up anywhere (grep: zero hits). | whole `src/` | Default-based emissions understated 1-30 % |
| F3 | Indirect (electricity) always added to SEE and certificate cost, every sector. Annex II: aluminium, steel, hydrogen count **direct only**. | `formulas.py:151` `total_see = (direct+indirect+precursor)/output`; `engine.py:255-257` cost uses `total_see` | Aluminium cost heavily overstated (Mozal demo 27.69 M EUR) |
| F4 | Precursor defaults used with no mark-up; demo supplement multiplies by 0.95. | `api/jobs.py:425`, `estimators.estimate_precursor_ee` | Not rule-based |
| F5 | Only aluminium + fertiliser logic. No cement, iron & steel, hydrogen models or CN codes. | `engine.py`, `lookup_tables.py` | 3 of 5 target sectors unsupported |
| F6 | Grid EF table has ZA, MZ, MA, EG only. No TZ. | `lookup_tables.py:186` | Tanzanian plant has no grid factor |
| F7 | No free-allocation (CBAM benchmark) deduction in certificate cost. Not in the doc formula, but required by Art. 31 / Reg. 2025/2620. | `formulas.cbam_certificate_cost_eur` | Cost overstated (small in 2026, phase-in) |
| F8 | No regulation version stored per factor (doc + recital 11: values revised by Dec 2027). | `lookup_tables.py` | Audit-trail gap |

## 2. Are the MVP values the official CBAM values?

**No.** `CBAM_DEFAULT_EMBEDDED` (`lookup_tables.py:104`) says itself "approximations ... replace with the official XLS",
and cites 2023/1773 (transitional reporting regulation, which has no default table). Compared with 2026/1740:

| CN | MVP total (dir / ind) | Official 2026/1740 | Note |
|---|---|---|---|
| 7601 10 00 unwrought Al | 8.6 (1.6 / 7.0) | MZ: 3.198 direct only, route K (primary) | 2.7x too high; indirect wrongly counted |
| 7601 20 00 Al alloys | 1.5 | MZ: 3.198 (7601 heading) | wrong |
| 2814 10 00 ammonia | 2.4 (2.1 / 0.3) | MA 2.200; TZ "–" → Other 3.130 | wrong |
| 3102 10 10 urea | 1.8 | code not in table; use 3102 10 19: MA 1.500, TZ 1.440 | wrong code + value |
| 2808 00 00 nitric acid | 2.4 | MA 2.540, TZ 1.680 | wrong |
| 3105 30 00 DAP | 1.0 (0.8 / 0.2) | MA 0.550, TZ 0.520 | ~2x too high |
| precursors (alumina, anode, AlF3, rock, potash, sulphur) | various | mostly not CBAM goods; values invented | wrong |

## 3. Is the PDF itself correct? (row by row against the OJ)

All values match 2026/1740 **except hydrogen**:

| Row | PDF | OJ | Verdict |
|---|---|---|---|
| Clinker 0.88, grey Portland 0.90, other hydraulic 0.86 | TZ | TZ (TARIC 2523100090 / 2523 29 00 / 2523900090) | OK |
| White Portland 1.45 | Other | TZ "–" → Other 1.300/0.140/1.450 | OK |
| Ammonia 3.13 | Other | TZ "–" → Other 2.970/0.150/3.130 | OK |
| Urea 3102 10 19 1.44, AN 1.80, nitric 1.68, NPK 0.82, DAP 0.52 | TZ | TZ | OK |
| **Hydrogen 10.820** | | **TZ has no 2804 row → Other countries = 17.740** | **WRONG** (10.820 is the figure in many other country tables) |
| Pig iron 3.480, 7207 11 14 / 7207 12 10 3.996, 7208 4.049 | Other | Other | OK |
| Al 7601 0.360, bars 0.830, profiles 0.840, sheets/foil 1.280 | TZ | TZ, route (L) = **secondary** aluminium | OK; note route L |
| Mark-up 10/20/30 %, fertilisers 1 %, applied to total column | | Annex I intro, verbatim | OK |

PDF nits: clinker and other hydraulic cement are 10-digit TARIC codes (2523100090, 2523900090), not "2523 10 00" / "2523 90 00".
Fallback rule (OJ, Annex I intro): country not listed, or field shows "–" → use "Other countries and territories".

## 4. Real company data found (public, free)

Self-reported, not CBAM-verified. Cement figures are corporate "kg CO2 / t cementitious, Scope 1 net",
a different boundary from CBAM SEE per CN code. Good as realistic seed values and sanity anchors, not as declared actuals.

| Sector | Company (country) | Value | Year | Source |
|---|---|---|---|---|
| Cement | Twiga / Tanzania Portland Cement (TZ, Heidelberg 69 %) | 506.29 kg CO2/t cement; AF substitution 22.9 % | 2025 | Twiga 2025 annual report, africanfinancials.com/document/tz-twiga-2025-ar-00 |
| Cement | Tanga Cement / Simba (TZ, Scancem/Heidelberg) | 512 kg CO2/t cementitious (Scope 1); 2030 target 454; 36 % low-clinker sales | 2025 | TCCL 2025 annual report, africanfinancials.com/document/tz-tccl-2025-ar-00 |
| Cement | Dangote Cement (group, incl. Mtwara TZ) | Scope 1: 570; Scope 1+2: 649 kg/t cementitious | 2024 | cement.dangote.com 2024 Sustainability Report |
| Cement | Lafarge Africa (NG) | 537 kg net CO2/t cementitious | 2024 | secondary summary, unverified |
| Cement | Heidelberg Materials group | 527 kg/t cementitious | 2024 | cemnet |
| Steel | ArcelorMittal South Africa | 2.90 tCO2e/t crude steel (2018 base), 2030 target 2.16 | 2023 roadmap | AMSA decarbonisation roadmap |
| Steel | Elmarakby Steel (EG) | 0.44 t CO2/t finished steel (direct + indirect, CBAM-style) | Q2 2025 | eurometal / GMK (secondary) |
| Steel | worldsteel route averages | scrap-EAF 0.69, DRI-EAF 1.47 t CO2/t crude steel | 2024 | worldsteel Sustainability Indicators |
| Aluminium | Mozal (MZ, South32) | process direct est. 1.76-1.90 tCO2e/t (third party). **On care & maintenance since 2026-03-15.** | FY25 | South32 AR 2025; mining.com 2026-03-16 |
| Aluminium | IAI | primary cradle-to-gate 4.5-22 tCO2e/t; anode ~0.43 t/t Al | 2025 | international-aluminium.org |
| Fertiliser | OCP (MA) | DAP est. ~0.76 tCO2e/t (third-party reconstruction) | 2026 | terawatttimes.org (low authority) |
| Fertiliser | IEA / EU ETS | SMR ammonia 1.8 tCO2/t (BAT); EU ETS benchmark 1.57 | | IEA Ammonia Roadmap |
| Hydrogen | none in TZ. Sasol Secunda coal H2 ~2.3 Mt/yr, no per-kg disclosure | | | Engineering News |

No public data found: Minjingu, ITRACOM (TZ fertiliser), ALAF, Lake Steel, Kamal Steel (TZ metals), Mbeya Cement,
Ezz Steel, Egyptalum, Hillside.

### Free bulk datasets
- Climate TRACE asset-level emissions (cement, steel, aluminium plants), CC-BY. Zenodo + BigQuery `trace-data-383422.climate_trace`. Modelled, not reported.
- APAD "Africa Cement Plants" on AWS Open Data (ODC-By): location, capacity, emissions. `aws s3 ls --no-sign-request`.
- GEM Global Cement & Concrete Tracker / Global Iron & Steel Tracker: plant list, capacity, route. Check licence.

### Paid (quote only, no public price)
- CDP Corporate Response Datasets (company-reported Scope 1/2): inquiry form at cdp.net/en/data-licenses.
- GCCA GNR 2.0 (cement, hosted by PwC): non-members get CO2 + clinker tabs; email gnrpmc@gccassociation.org.
- Real CBAM actuals exist only as installation data from the operator (EU Communication template). Best route: a pilot with Twiga or Tanga Cement.

## 5. Recommended fixes (not done)
1. Add a default-values path: `qty × total × (1 + markup(sector, year))`, loaded from the CSV, with `reg_version = "2026/1740"` per row.
2. Drop indirect from SEE and cost for aluminium, steel, hydrogen.
3. Replace `CBAM_DEFAULT_EMBEDDED` with the official per-country table ("–" → Other fallback). Fix the urea CN code.
4. Add TZ grid EF; add cement, steel, hydrogen CN codes.
5. Correct hydrogen in the PDF to 17.740.
6. Demo: Mozal is idle since 2026-03-15. A Tanzanian cement profile (Twiga-like, ~506 kg/t) is a more realistic demo.
