# Tanzanian manufacturers: real data vs CBAM defaults (2026-11-20)

Data rows: [tz_sme_real_data_2026-11-20.csv](tz_sme_real_data_2026-11-20.csv) (each row has `data_quality` + source).
Defaults: [cbam_defaults_2026_1740_TZ_and_other.csv](cbam_defaults_2026_1740_TZ_and_other.csv).

## Who the Tanzanian producers are (by CBAM sector)
| Sector | Companies | Public emissions data? |
|---|---|---|
| Cement | Twiga (TPC, Heidelberg), Tanga/Simba (Scancem/Heidelberg), Dangote Mtwara, Lake/Nyati, Mbeya, Camel, Kilimanjaro, Kisarawe, Huaxin/Maweni, Hengya | Twiga + Tanga only (DSE-listed, IFRS S2 disclosures). SMEs: none |
| Iron & steel | Lodhia (billets + rebar), Kamal Steel (scrap rebar, 80 kt), Steelmasters, MMI, GSM (new long-steel complex) | none; capacities only |
| "Aluminium" | ALAF: actually Al-Zn **coated steel** coil (CN 7210 = steel sector), substrate imported | none |
| Fertilisers | ITRACOM (organo-mineral, 1 Mt, Dodoma), Minjingu (phosphate rock + NPK) | none; check CN scope (2510, 3101 not CBAM) |
| Hydrogen | none industrial (Kilwa cooking pilot only) | n/a |

Real SME emissions disclosures do not exist publicly in Tanzania. Only the two listed cement companies publish numbers,
because DSE/NBAA now requires IFRS S2 sustainability disclosure.

## Best real data: Twiga 2025 (primary, audited annual report)
- Scope 1: 923,000 tCO2e = 506.29 kg/t cement
- Scope 2: 58,537 tCO2e = 32.11 kg/t, location-based, grid EF 0.336 kg CO2/kWh (UNFCCC IFI 2021)
- Derived: ~1.82 Mt cement, ~174 GWh grid power, ~96 kWh/t
- Direct + indirect ≈ **0.538 t/t** vs TZ default grey Portland **0.900 × 1.10 = 0.990** (2026)
  → actual data cuts embedded emissions ~46 %. That gap is the product's value proposition.
- Caveat: company boundary (includes quarry diesel, onsite power; biomass excluded), not CBAM installation/CN boundary.

Tanga 2025: Scope 1 512 kg/t cement (coal kiln). Same grid EF cited.

## Steel SMEs: default is brutal
TZ has no steel rows → "Other countries" BF-BOF route (C) applies: rebar 7214 20 00 and billets 7207 = **3.996 × 1.10 = 4.40 t/t** in 2026.
TZ mills are scrap-based (induction/EAF). Validation from elsewhere:
- worldsteel scrap-EAF avg 0.69 t CO2/t (scope 1+2); CBAM counts direct only, so lower still
- Indian induction melting 800-900 kWh/t (indirect, not counted for steel); rolling 3.13 GJ/t, ~0.36 t CO2/t (TERI)
- Elmarakby (EG) 0.44 t/t direct+indirect, CBAM-style voluntary report
→ Plausible direct SEE for a TZ scrap rebar mill: ~0.1-0.4 t/t vs 4.40 default. 10x gap.

## Fertiliser SMEs
TZ defaults: NPK 3105 20 10 = 0.820, 3105 90 80 = 0.550, 3105 10 00 = 0.680 (× 1.01).
Blending plants emit almost nothing on site (2.8-4.5 kWh/t blending; granulation ~40-60 kWh/t + steam);
embedded emissions come from imported precursors (urea, DAP, AN), which need supplier data or precursor defaults.
Check CN scope first: phosphate rock (2510) and organic fertilisers (3101) are outside CBAM.

## What to do with this in the MVP
1. Add TZ grid EF 0.336 kg/kWh (source: UNFCCC IFI 2021, as used by Twiga/Tanga).
2. Build a Twiga-like demo profile: 1.82 Mt cement, 506 kg/t scope 1, 96 kWh/t, 22.9 % AF. Show actual (0.54) vs default (0.99).
3. Build a scrap-rebar SME profile (Kamal-like, 80 kt/yr) showing default 4.40 vs actual.
4. Getting true SME data needs the operator: offer a free "default vs actual" assessment to Kamal/Lodhia/Camel/Kilimanjaro.
   No public or purchasable dataset has Tanzanian SME plant data (CDP/GNR only cover large reporters).

## Sources
- TPCPLC Annual Report & AFS 2025 (dse.co.tz/storage//securities/TPCC/financial_statement/Annual/v6jUZTp63Lkk0lKx32dLYeX9cZV4giVsMkuWx73y.pdf)
- TPCPLC Integrated Annual Report 2023 (twigacement.com/sites/default/files/2024-09/Annual Report 2023 (English & Swahili).pdf)
- Tanga Cement Report & AFS 2025 (dse.co.tz/storage//securities/TCPLC/financial_statement/Annual/fi0Irn3XKnRsLgtvLPGuCVRZysn1tOS9SeoTJMPl.pdf)
- Fastmarkets East Africa special report; IFC disclosure 46058 (Kamal Steel); lodhiaindustries.com; Danieli
- tanzaniainvest.com (ITRACOM); IFDC register (Minjingu); thecitizen.co.tz (ALAF, Kilwa H2)
- worldsteel Sustainability Indicators 2025; TERI ES2014IE04; CEEW; eurometal.net (Elmarakby)
