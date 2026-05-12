# 01 — What the Pipeline Outputs

A full run produces artefacts at four layers: ERPNext records, raw JSONL landings, the canonical SQLite store, and the final CBAM reports.

> **Want to see these outputs yourself before reading more?** Jump to [02_SETUP_AND_RUN.md](02_SETUP_AND_RUN.md), run the pipeline, then come back.

---

## Layer 1 — ERPNext records (live, browsable at `http://localhost:8080`)

After `python -m scripts.seed_erpnext --profile mozal_aluminium`:

| Doctype | Approx. count per profile | What it contains |
|---|---|---|
| **Custom Fields** | 21 | `custom_cn_code`, `custom_facility_code`, `custom_sector`, `custom_eu_export_share`, `custom_scrap_rate_pct`, `custom_supplier_country`, `custom_recycled_content_pct`, `custom_invoice_category` … |
| **UOMs** | 5 | tonnes, Nm³, litres, kg, kWh |
| **Item Groups** | 4 | raw_material, fuel, feedstock, finished_good |
| **Items** | 10 | Finished goods (e.g. AL-INGOT-P1020 / UREA-PRILLED) + precursors (alumina, anode, AlF3, phosphate rock, sulphur) + fuels (NG, diesel, HFO, LPG), each tagged with its CBAM CN code |
| **Suppliers** | 7–9 | Alunorte (BR), Worsley (AU), Qatargas (QA), Uralkali (RU), OCP Khouribga (MA) … with ISO country codes |
| **Customers** | 5 | EU importers (Norsk Hydro, Yara, Borealis, Eurochem, Speira …) |
| **Cost Centres** | 5 | potline_1, potline_2, anode_plant, casthouse, utilities (Mozal); smr_unit, urea_unit, nitric_acid_unit, dap_unit, utilities (OCP) |
| **BOMs** | 2–4 | One per finished good with physically-realistic ratios (1.925 t alumina + 0.43 t anode + 0.018 t AlF3 per t Al) |
| **Work Orders** | ~1,440 (24 mo × 60) | Planned + actual dates, produced_qty, status, CN code, EU export share, scrap rate |
| **Rework Work Orders** | ~17 (1.2 % rate) | Child WOs linked to their parent run |
| **Purchase Orders** | ~960 | Stoichiometrically sized from BOM × planned monthly output, with seasonality + price drift |
| **Purchase Invoices** | ~575 (60 % of POs) | Linked to originating PO, supplier country, CBAM invoice category |
| **Stock Entries** | ~1,430 | `Manufacture` type — Work Order → finished-good qty + UOM (MSEG equivalent) |
| **Quality Inspections** | ~1,440 | One per Work Order, status `Accepted` or `Rejected` |
| **Sales Invoices** | ~144 (Mozal) / ~288 (OCP) | One per (product × month × EU customer), denominated in EUR |
| **GL Entries** | auto-posted | ERPNext writes them on every submitted Purchase / Sales Invoice — available for the finance-reconciliation pass |

The SeedReport prints to stdout:

```
[seed:mozal_aluminium] items=10 suppliers=10 customers=5 cost_centres=5 boms=2
                       wo=1442 rework=18 po=956 pinv=574 stock=1380 qa=1442
                       sinv=144 errors=0
```

A `.env.erpnext` file is written to the project root with auto-generated API key + secret (chmod 600) so the ingestion CLIs can pick them up.

---

## Layer 2 — Raw JSONL landings (`data/raw/`)

After `python -m scripts.run_erpnext_pipeline`:

```
data/raw/
├── erpnext/
│   ├── production_runs/20260511T093212.jsonl       (~1,440 rows)
│   ├── purchase_orders/20260511T093212.jsonl       (~960 rows)
│   ├── bill_of_materials/20260511T093212.jsonl     (~8 rows)
│   └── invoices/20260511T093212.jsonl              (~575 rows)
├── manual/
│   ├── facility/20260511T093215.jsonl              (1 row)
│   ├── sensor_reading_manual/20260511T093215.jsonl (1 row)
│   └── supplier_portal_submission/20260511T093215.jsonl (1 row)
└── ocr/
    └── ocr_invoices/20260511T093217.jsonl           (1 row)
```

One JSONL row per record, each line a canonical-shape dict (identical structure whether the producer was the direct REST runner or an Airbyte File destination). Sample `production_runs` row:

```json
{
  "run_id": "WO-MFG-1423",
  "facility_id": "MOZAL-MZ-01",
  "sector": "aluminium",
  "product_name": "AL-INGOT-P1020",
  "product_cn_code": "76011000",
  "batch_no": "WO-MFG-1423",
  "output_tonnes": 712.4,
  "scrap_rate_pct": 1.18,
  "eu_export_share": 0.617,
  "run_started_at": "2026-04-15T08:00:00",
  "run_ended_at": "2026-04-15T22:00:00",
  "shift_supervisor": "Administrator"
}
```

These files are **replay-safe**: re-running the same window produces a new timestamped file; nothing overwrites.

---

## Layer 3 — Canonical SQLite store (`data/carbontrace.db`)

20 tables. After a full Mozal + OCP run:

| Table | Approx. rows | What it holds |
|---|---|---|
| `production_runs` | ~2,900 | One per Work Order; CN code, output tonnes, EU export tonnes, allocation method, outcome |
| `energy_consumption` | ~700 | Fuel POs (mapped) + manual electricity meter readings |
| `precursor_purchases` | ~1,500 | Non-fuel POs with CN code + supplier country + qty |
| `facilities` | 1+ | The onboarded facility/ies |
| `aluminium_process` | varies | Anode consumption, AE minutes, primary Al output (manual) |
| `fertiliser_process` | varies | NH3 SMR, urea, HNO3 fields (manual) |
| `supplier_portal` precursor rows | 1+ | Block E.7 actual EE submissions |
| `invoice_documents` | 1+ | OCR-extracted invoices |
| `monitoring_meta` | 1+ | Tier, GWP set, verifier, opinion, uncertainty (manual) |
| `process_boundary` | optional | One per (facility × product) if manual form filled |
| `recs_certificates` | optional | One per certificate ingested |
| `chp_records` | optional | If CHP form filled |
| `carbon_price_paid` | optional | Block G; populated for SA only by direction |
| `mr_plans` | optional | Monitoring & Reporting Plan |
| `cost_centre_allocation` | optional | Sub-process electricity allocations |
| `stock_movements` / `gl_entries` / `quality_inspections` | empty today | Models exist; ingestion mappers not yet wired (1-day fix each) |
| `outbound_shipments` | empty today | Modelled, mapper not wired |
| `fugitive_emissions` | optional | Manual annual form |
| `ingestion_events` | one per ingestor invocation | Audit trail: which source ran when, in/ok/err counts |

Each table has the canonical Pydantic payload as JSON plus indexed columns (`id`, `source`, `ingested_at`, `facility_id`, `period_start/end`, `raw_ref`).

Query directly:

```bash
sqlite3 data/carbontrace.db "SELECT facility_id, COUNT(*) FROM production_runs GROUP BY facility_id;"
```

---

## Layer 4 — Final CBAM reports (`data/reports/`)

After `python -m scripts.run_calculation 2026-Q2`:

```
data/reports/
├── cbam_quarterly_<run_id>.xml      (EU CBAM IT-Tools shape)
├── cbam_quarterly_<run_id>.csv      (one row per facility × CN × quarter)
└── dashboard_<run_id>.json          (pre-aggregated for the UI)
```

### A. CBAM XML — what the EU declarant uploads

```xml
<?xml version='1.0' encoding='utf-8'?>
<ns0:QuarterlyReport xmlns:ns0="urn:eu:cbam:quarterly-report:v1" runId="…">
  <Installation>
    <OperatorName>Mozal SA</OperatorName>
    <FacilityId>MOZAL-MZ-01</FacilityId>
    <CbamInstallationId>MZ-INST-001</CbamInstallationId>
    <EORI>MZ100123456789</EORI>
    <UNLOCODE>MZMPM</UNLOCODE>
    <Country>MZ</Country>
    <Sector>aluminium</Sector>
    <Quarter>2026-Q2</Quarter>
    <ReportingPeriodStart>2026-04-01</ReportingPeriodStart>
    <ReportingPeriodEnd>2026-06-30</ReportingPeriodEnd>
    <Goods>
      <Good cnCode="76011000">
        <ProductName>Primary Aluminium Ingot</ProductName>
        <OutputTonnes>50000.000</OutputTonnes>
        <EUExportTonnes>30000.000</EUExportTonnes>
        <DomesticSalesTonnes>20000.000</DomesticSalesTonnes>
        <EmbeddedEmissions>
          <DirectSEE>1.6281</DirectSEE>
          <IndirectSEE>0.4400</IndirectSEE>
          <TotalSEE>4.0841</TotalSEE>
          <AdjustedSEE>2.9950</AdjustedSEE>
          <OverallUncertaintyPct>4.49</OverallUncertaintyPct>
          <ShareOfEstimatedEmissions>0.3632</ShareOfEstimatedEmissions>
        </EmbeddedEmissions>
        <CarbonPricePaidEURPerTCO2e>20.0000</CarbonPricePaidEURPerTCO2e>
        <AllocationMethod>mass</AllocationMethod>
        <AllocationShare>1.0000</AllocationShare>
        <EmissionLines>
          <Line category="process" tier="ipcc_default" estimated="true">
            <Label>Pre-bake anode CO2</Label>
            <Activity>21500.000 tonnes</Activity>
            <EF>1.0000 tCO2e/unit</EF>
            <EFSource>IPCC V3 Ch4 Eq 4.20 (pre-bake)</EFSource>
            <CO2eTonnes>74175.0000</CO2eTonnes>
            <UncertaintyPct>5.00</UncertaintyPct>
          </Line>
          <!-- 5–15 more lines: PFCs, electricity, REC-adjusted electricity, precursors, fugitives -->
        </EmissionLines>
      </Good>
    </Goods>
    <Totals>
      <DirectEmissionsTCO2e>81407.280</DirectEmissionsTCO2e>
      <IndirectEmissionsTCO2e>22000.000</IndirectEmissionsTCO2e>
      <PrecursorEmissionsTCO2e>100800.000</PrecursorEmissionsTCO2e>
      <TotalEmissionsTCO2e>204207.280</TotalEmissionsTCO2e>
      <ProjectedCBAMCostEUR>6738840.24</ProjectedCBAMCostEUR>
    </Totals>
    <Reconciliation>
      <MassBalanceResidualPct>3.21</MassBalanceResidualPct>
      <EnergyBalanceResidualPct>5.84</EnergyBalanceResidualPct>
    </Reconciliation>
    <EstimationFlags>
      <ProductOver20pctEstimated>76011000</ProductOver20pctEstimated>
    </EstimationFlags>
  </Installation>
</ns0:QuarterlyReport>
```

Every CBAM IR 2023/1773 Section 1 / 2 / 3 / 5 / 6 / 7 / 8 / 9 tag is populated. The `EmissionLines` block gives the verifier traceable provenance per emission contribution (category, tier, EF source citation, uncertainty, estimated flag).

### B. CBAM CSV — flat dashboard-ready table

```csv
run_id,quarter,facility_id,country,sector,cn_code,product_name,output_tonnes,
eu_export_tonnes,domestic_sales_tonnes,direct_tco2e,indirect_tco2e,
precursor_tco2e,direct_see,indirect_see,total_see,adjusted_see,
overall_uncertainty_pct,share_estimated,carbon_price_paid_eur,eua_price_eur,
allocation_method,allocation_share,cbam_certificate_cost_eur

<run_id>,2026-Q2,MOZAL-MZ-01,MZ,aluminium,76011000,Primary Aluminium Ingot,
50000.0,30000.0,20000.0,81407.28,22000.0,100800.0,1.6281,0.44,4.0841,2.995,
4.49,0.3632,20.0,75.0,mass,1.0,6738840.24
```

One row per `(run × facility × CN × quarter)`. Ready to load into any BI tool, pivot in Excel, or pipe into a Postgres warehouse for trending.

### C. Dashboard JSON — pre-aggregated for the UI

```json
{
  "runId": "<uuid>",
  "generatedAt": "2026-05-11T02:38:00",
  "facilities": [{
    "facilityId": "MOZAL-MZ-01",
    "name": "Mozal SA",
    "country": "MZ",
    "sector": "aluminium",
    "quarter": "2026-Q2",
    "totals": {
      "directTCO2e": 81407.28,
      "indirectTCO2e": 22000.0,
      "precursorTCO2e": 100800.0,
      "totalTCO2e": 204207.28,
      "projectedCBAMCostEUR": 6738840.24,
      "euExportShare": 0.60
    },
    "reconciliation": {
      "massBalanceResidualPct": 3.21,
      "energyBalanceResidualPct": 5.84,
      "financeResidualPct": null
    },
    "estimationFlags": ["76011000"],
    "products": [{
      "cn": "76011000",
      "name": "Primary Aluminium Ingot",
      "outputT": 50000, "euExportT": 30000,
      "directSEE": 1.6281, "indirectSEE": 0.4400,
      "totalSEE": 4.0841, "adjustedSEE": 2.9950,
      "uncertaintyPct": 4.49, "shareEstimated": 0.3632,
      "carbonPricePaidEUR": 20.0, "cbamCostEUR": 6738840.24,
      "allocation": {"method": "mass", "share": 1.0},
      "lines": [
        {"category": "process", "label": "Pre-bake anode CO2",
         "activity": 21500.0, "activityUnit": "tonnes",
         "ef": 1.0, "efUnit": "tCO2e/unit",
         "tier": "ipcc_default", "source": "IPCC V3 Ch4 Eq 4.20 (pre-bake)",
         "co2e": 74175.0, "uncertaintyPct": 5.0, "estimated": true},
        {"category": "process", "label": "PFCs (CF4 + C2F6)", "...": "..."},
        {"category": "electricity", "label": "Electricity (potline_1) (REC-adjusted)", "...": "..."},
        {"category": "precursor", "label": "Precursor CN 28182000",
         "tier": "supplier_actual", "co2e": 100800.0, "estimated": false}
      ]
    }]
  }]
}
```

This is what a dashboard layer would render directly — every number on the screen has provenance, every chart can drill into the emission-line breakdown.

### D. Console summary

```
CBAM run 88927752-38ab-4ffe-8bbb-0c769e51ed50
  facilities       : 1
  total products   : 1
  • MOZAL-MZ-01 [2026-Q2]  total=204,207 tCO2e  CBAM cost=€6,738,840  flagged_products=1
      ↳ CN 76011000  out=50,000t  SEE=4.084  adj=2.995  ±4.5%  est-share=36.3%

Artefacts:
  xml : data/reports/cbam_quarterly_<run_id>.xml
  csv : data/reports/cbam_quarterly_<run_id>.csv
  json: data/reports/dashboard_<run_id>.json
```

---

## What the verifier sees

For a CBAM-accredited verifier doing a sign-off, the audit trail at the end of one run is:

1. **CBAM XML** with every required Annex IV / VIII section populated
2. **Per-emission-line breakdown** with category, activity quantity + unit, EF value + unit, tier (measured / supplier_actual / national / cbam_default / ipcc_default / estimated), **citable source string**, CO₂e contribution, uncertainty %
3. **Reconciliation residuals** — mass balance, energy balance, finance cross-check (when GL pull is wired)
4. **Estimation flag** when any product exceeds the 20% estimated-share threshold per CBAM IR Art.4(3)
5. **Underlying ERPNext records** browsable at `http://localhost:8080` (Work Orders → BOMs → Stock Entries → POs → Suppliers → Purchase Invoices), all with real FKs
6. **`ingestion_events` audit table** showing every ingestion run with timestamps + in/ok/err counts
7. **Raw JSONL landings** preserved per sync — replayable for any historical period
8. **`raw_ref` on every canonical row** — back-pointer to the source JSONL line → ERPNext document name

---

## What the dashboard sees

Reads `dashboard_<run_id>.json` directly. Already-computed:

- Per-facility totals (direct / indirect / precursor / total tCO₂e, projected CBAM EUR cost, EU export share)
- Reconciliation residuals (mass / energy / finance %)
- Per-product breakdown (output tonnes, EU export tonnes, direct/indirect/total/adjusted SEE, uncertainty, share-estimated, allocation method)
- Per-emission-line breakdown for drill-down charts (Sankey, contribution bars)
- Estimation-flag list for the data-quality panel

No extra aggregation needed at the UI layer — the JSON is shape-ready for any chart library.

---

## What's NOT produced yet (honest gaps)

| Output | Why missing | How far away |
|---|---|---|
| `gl_entries` table populated | ERPNext auto-posts them; we don't pull them yet | One mapper in `ERPNextRunner` (~50 lines) |
| `stock_movements` table populated | Stock Entries written by seeder; not pulled by the runner | Same |
| `outbound_shipments` table populated | Sales Invoices written; mapper not added | Same |
| Live EUA spot price | Static `€75/tCO2e` | One HTTP fetch from ICE |
| Live FX rates | Static table | One HTTP fetch from ECB |
| XSD-validated XML | Official CBAM XSD not yet published by the Commission | Validation pass when the XSD lands |
| Steel & hydrogen sector runs | MVP scope is Al + fertiliser | Add two engine branches |
| Charts / dashboard UI | JSON is ready; no UI component built | UI is the next deliverable — see [03_ROADMAP.md](03_ROADMAP.md) |

---

## TL;DR — what you get when you press "run"

| File / record | Where | Purpose |
|---|---|---|
| ~5,000 ERPNext records | http://localhost:8080 | A real ERP, browsable by funder / auditor |
| ~4,000 JSONL rows | `data/raw/erpnext/**/*.jsonl` | Replay-safe raw landing zone |
| ~5,000 canonical rows across 20 SQLite tables | `data/carbontrace.db` | Single source of truth for downstream layers |
| 1 CBAM XML | `data/reports/cbam_quarterly_<run>.xml` | What the EU declarant uploads to the CBAM portal |
| 1 dashboard CSV | `data/reports/cbam_quarterly_<run>.csv` | One row per facility × product × quarter; pivot-ready |
| 1 dashboard JSON | `data/reports/dashboard_<run>.json` | Pre-aggregated, chart-ready, full per-line breakdown |
| Console summary | stdout | Verified Mozal Q2 numbers: 204k tCO2e, SEE 4.084, adj SEE 2.995, CBAM cost €6.74M, ±4.5%, 36.3% estimated |

Every number in every output has a back-pointer (`raw_ref`) to the JSONL line, which has a back-pointer to the ERPNext document name, which has a real database row a verifier can open in their browser.
