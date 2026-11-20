# MVP inventory, factor validity, ISSB (Tanzania) coverage (2026-11-20)

Code audited: main checkout `carbonTraceAI_mvp/` (branch `main`, uncommitted). Read-only; nothing changed.

## 1. What the MVP does

| Layer | What it does | Files |
|---|---|---|
| ERP sandbox | ERPNext in Docker, seeded with 2 fake factory profiles: `mozal_aluminium` (MZ smelter), `ocp_fertiliser` (MA ammonia/urea/DAP/HNO3). 24 months of Work Orders, POs, invoices, BOMs. | `src/seeding/`, `scripts/seed_erpnext.py` |
| Ingestion | ERPNext REST (+ Airbyte option), manual web forms, supplier portal (precursor actual EE), OCR of utility/fuel invoices (Tesseract not installed) | `src/ingestion/`, `src/onboarding/` |
| Canonical store | SQLite, Pydantic models, ~20 tables, ingestion audit log | `src/storage/`, `src/core/models.py` |
| Calc engine | **Actual-emissions method only** per CN code per quarter: fuel combustion (IPCC Tier 1), aluminium process (anode CO2 + PFC), fertiliser process (SMR CO2, HNO3 N2O), fugitive (refrigerants, SF6, flaring), electricity × grid EF, steam, REC deduction, precursors (supplier actual or default), uncertainty propagation, EF tier priority, coproduct allocation | `src/calculation/` |
| Cost | `certificate cost = SEE_total × (1 − carbon price paid / EUA) × EU-export t × EUA` | `formulas.py:155-173` |
| Outputs | "CBAM quarterly report" XML (own namespace `urn:eu:cbam:quarterly-report:v1`), CSV, dashboard JSON | `renderer.py` |
| Market data | FX live from ECB (Frankfurter); EUA price static €75 (env override) | `market_feeds.py` |
| UI | Next.js dashboard: runs, emission split (Scope 1 · Scope 2 · Precursors), audit, reports | `frontend/` |

Scope stated in README: EU CBAM only; aluminium (MZ, ZA) and fertilisers (MA, EG). No cement, steel, hydrogen. No Tanzania.

## 2. Every value it uses, and whether it is valid

### Correct (matches source)
| Value | MVP | Source check |
|---|---|---|
| Fuel NCV + CO2 EF (IPCC 2006 V2 Ch1 T1.2/1.4) | diesel 43.0 GJ/t, 74.1 kg/GJ; HFO 40.4, 77.4; LPG 47.3, 63.1; bituminous coal 25.8, 94.6; coke 28.2, 107.0; NG 56.1 kg/GJ; wood 15.6 | match IPCC defaults |
| AR5 GWPs | CH4 28, N2O 265, CF4 6630, C2F6 11100, SF6 23500 | match AR5 |
| SMR feedstock CO2 | 1.96 kg CO2/Nm3 NG | stoichiometric CH4 (0.717 kg/Nm3 × 44/16 ≈ 1.97). OK |
| PFC slope CF4 | prebake 0.143, Søderberg 0.272 kg/t/(AE-min/cell-day) | match IPCC / EU MRR / US 40 CFR 98 F-1 |
| Carbon-price-paid deduction | concept present | CBAM Art. 9. OK in principle |
| EF priority measured > supplier > national > default | | sensible |

### Wrong or not CBAM-compliant
| # | Item | MVP | Should be | Effect |
|---|---|---|---|---|
| V1 | **GWP set default** | `gwp_set = "AR6"` (`engine.py:68`) | **AR5**, per Commission CBAM Guidance No. 3 (in line with EU ETS) | N2O, PFC, CH4 slightly off; not CBAM-conformant |
| V2 | **Gases counted** | refrigerants (HFCs), SF6, flaring CH4 in direct emissions | CBAM Annex I: CO2 for all goods; + N2O (fertilisers); + PFCs (aluminium). No HFC/SF6/CH4 | Over-counts |
| V3 | **Indirect in SEE/cost for aluminium** | always added | Annex II: Al, steel, H2 direct only | Big over-count for Al |
| V4 | **CBAM default table** | invented values, cites 2023/1773 | Reg. 2025/2621 as replaced by **2026/1740** | Wrong (details in audit note) |
| V5 | **Mark-up** | none | 10/20/30 %, fertilisers 1 % | Default path understated |
| V6 | **Free-allocation adjustment** | none | Certificates = embedded − (CBAM factor 97.5 % in 2026 × CSCF × CBAM benchmark × qty) | **Cost massively overstated.** In 2026 most of the benchmark share is deducted. €27.69M Mozal cost is not a real CBAM liability |
| V7 | PFC slope C2F6 | 0.0121 used as a slope (`lookup_tables.py:143`) | C2F6 = SEF_CF4 × F_C2F6 = 0.143 × 0.121 = **0.0173** (prebake); Søderberg 0.272 × 0.252 = 0.0685 | C2F6 under-counted ~30 % (prebake), ~7× (Søderberg) |
| V8 | PFC Tier 1 defaults | prebake CF4 0.04, C2F6 0.004 kg/t | IPCC 2006 Table 4.15 CWPB: CF4 0.4, C2F6 0.04 (newer 2019 Refinement values differ). **Not verified which edition the MVP intends** | possibly 10× low |
| V9 | Anode CO2 factor | 3.45 kg CO2/kg (comment says 85 % C, S 2 %, ash 0.4 %) | IPCC Eq 4.21 with S 2 %, ash 0.4 % → (1 − 0.024) × 44/12 = **3.58**; with 85 % C → 3.12. Value matches neither | ~4 % low; internally inconsistent |
| V10 | Oxidation factor | 0.98-0.99 for liquids/solids | IPCC 2006 Tier 1 default = 1.0; CBAM calculation method uses 1 unless measured (**verify in CBAM monitoring annex**) | 1-2 % low |
| V11 | Urea CO2 | process CO2 netted by `co2_captured_tco2` (`engine.py:361`); `UREA_CO2_USED_PER_T = 0.78` | stoichiometric 44/60 = **0.733**. EU ETS does not let CO2 bound in urea be deducted; CBAM is expected to follow (**not confirmed in final EU text, verify**) | Fertiliser emissions likely under-counted |
| V12 | HNO3 N2O no-abatement | 7.5 kg/t | IPCC 2006 Table 3.3 ranges 5 (atmospheric) to 9 (high pressure) by plant type; single value is a rough mid-point | OK as a placeholder only |
| V13 | Grid EFs | ZA 0.90, MZ 0.04, MA 0.62, EG 0.45 kg/kWh, no source year; **no TZ** | TZ: 0.336 (UNFCCC IFI 2021, used by Twiga/Tanga). Others need sourcing (IEA/IFI) | TZ missing |
| V14 | NG NCV | 39.0 GJ/1000 Nm3 | depends on gas; typical NCV 34-38. "Carbon content 75 % by volume" is meaningless | minor |
| V15 | Biomass | EF 0 always | CBAM zero-rates biomass only if RED II sustainability criteria are met | Over-generous |
| V16 | 20 % estimation threshold | cites "CBAM IR Art.4(3)" (2023/1773) | transitional-period rule (ended 31 Dec 2025). Definitive period: actual or default only | Obsolete flag |
| V17 | Report format | own XML namespace "quarterly report" | Quarterly reports ended with the transitional period. Definitive: annual CBAM declaration by authorised declarant (first for 2026, due 30 Sep 2027); operator side gives importers the **communication template** with verified data | Main output not an official format |
| V18 | Coproduct allocation | mass / energy / **economic** | CBAM attributes emissions by production process; economic allocation is not a CBAM method (**verify**) | |
| V19 | EUA price | static €75 | 2026: Commission publishes quarterly average of EUA auction prices; weekly from 2027 | Stale |
| V20 | Precursor list | alumina, anode, AlF3, phosphate rock, potash, sulphur | only CBAM goods count as relevant precursors (e.g. alumina 2818 20 for Al; ammonia, nitric acid, urea for fertilisers) | Over-counts with invented values |
| V21 | Demo data | Mozal profile | Mozal on care and maintenance since 2026-03-15; data synthetic | Demo only |

**Verdict:** Ingestion, data model, audit trail and UI are usable. The calc chain mixes correct IPCC fuel factors with non-CBAM scope (gases, indirect for Al), outdated transitional-period rules, and no default/mark-up/free-allocation logic. Its output is **not a valid CBAM number or cost** in the definitive period.

## 3. Does it cover ISSB (IFRS S1/S2) for Tanzania?

**No.** No IFRS/ISSB/S1/S2/TFRS reference, output or data field anywhere in `src/`, `frontend/`, `config/`, `docs/`.
The only overlap is labelling: CBAM direct/indirect is shown as "Scope 1 · Scope 2" in the UI.

### Tanzanian ISSB rules (primary sources read)
- **NBAA Technical Pronouncement No. 1 of 2024** (July 2024): adopts IFRS S1, IFRS S2 and all future ISSB standards.
  Mandatory for **public interest entities + public sector** for periods from **1 Jan 2025**.
- **PIE definition** (IFRS jurisdiction profile, 12 Jun 2025):
  - listed debt or equity;
  - fiduciary holders (banks, insurers, funds);
  - commercial entities with gross capital ≥ **TZS 50 bn** in essential or strategic goods (power, petroleum/gas, water, telecoms, transport, extractives, food).
  - Other entities: **permitted, not required.**
- **Scope 3 relief:** phased from 2026; Category 15 from 2028; all categories by 2029.
- **Placement:** inside the "Report by those charged with governance" (TFRS 1), same time as the financial statements. Explicit statement of compliance with ISSB required. No local modifications.
- **Assurance:** auditors apply ISA 720 (consistency check) for now. **NBAA Technical Pronouncement No. 1 of 2026** (approved 30 Jul 2026, effective FY from **1 Jan 2027**):
  - disclosures sit under a "Sustainability Disclosures" heading;
  - optional stand-alone report;
  - entities and audit firms must run **ISSA 5000 readiness assessments**;
  - date for assurance to be announced.
- **Banks:** Bank of Tanzania 2025 guidelines require ISSB application by banks and financial institutions. They will ask borrowers for emissions data.
- DSE Rules 2022 also permit ESG reporting under ISO 26000 / GRI.

### Who this hits in our target list
| Company | ISSB status |
|---|---|
| Twiga, Tanga Cement | **in scope** (DSE-listed). Already disclosing Scope 1/2 under IFRS S2 transitional relief in FY2025 reports |
| Large private cement or steel firms (Lodhia, Dangote TZ, Mbeya/Amsons, Huaxin) | in scope only if listed or if they meet the TZS 50 bn + "essential goods" test. Manufacturing is not named in the list, so likely **voluntary** |
| SMEs | not required. But **indirectly affected**: listed customers' Scope 3 phase-in (2026-2029) and bank (BoT) climate-risk data requests will ask them for emissions |

### Gap: what the MVP would need for IFRS S2 (TZ)
1. **Entity-level GHG inventory** under the GHG Protocol: organisational boundary (control/equity), all gases, Scope 1, Scope 2 location- **and** market-based, Scope 3 by category. The CBAM installation/product boundary is not the same thing.
2. Industry metrics from SASB, e.g. EM-CM (cement), EM-IS (steel), RT-CH (chemicals/fertiliser).
3. Narrative modules: governance, strategy, climate risks and opportunities, scenario analysis, transition plan, targets (cross-industry metrics, internal carbon price, capital deployment).
4. Output in TFRS 1 "Sustainability Disclosures" layout plus an ISSA 5000-ready audit trail (the existing ingestion audit log helps here).
5. Reuse of existing work: activity data, IPCC fuel factors, the grid EF table (add TZ 0.336) and the uncertainty engine carry over directly.

## Sources
- NBAA Technical Pronouncement No. 1 of 2026 (nbaa.go.tz, Aug 2026); NBAA notice "Taarifa ya Kiufundi Na. 1 ya 2026"
- IFRS Foundation jurisdictional profile: Tanzania (updated 12 Jun 2025)
- Commission CBAM Guidance No. 3 (AR5 GWPs); Guidance No. 4 (free allocation adjustment)
- Reg. 2023/956 Annex I/II; Reg. 2026/1740 (defaults, mark-ups)
- IPCC 2006 Guidelines V2 Ch1, V3 Ch3-4; US 40 CFR 98 Table F-1 (PFC slope/F_C2F6)
- cbamguide.com / ohESG (CBAM factor 97.5 % for 2026, CSCF)
