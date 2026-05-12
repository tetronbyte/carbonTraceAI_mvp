# 02 — Setup & Run

From a clean machine to a verified CBAM report in 6 commands.

> All commands assume the project root: `/path/to/carbonTraceAI_mvp/`. The repo is self-contained; no external services required for the calc-engine smoke test path.

---

## 0. Prerequisites

| Tool | Version | Why | macOS install |
|---|---|---|---|
| Python | 3.12+ | Runtime | `brew install python@3.12` |
| Docker Desktop | 4.30+ | ERPNext sandbox | https://www.docker.com/products/docker-desktop |
| Tesseract | 5.x | OCR (invoice extraction) | `brew install tesseract` |
| ngrok | latest | Remote-demo tunnel (optional) | `brew install ngrok` |
| Git | any | Cloning | usually pre-installed |

On Linux:
```bash
sudo apt update && sudo apt install -y python3.12 python3.12-venv tesseract-ocr
# Docker: https://docs.docker.com/engine/install/
```

Verify:
```bash
python3 --version            # >=3.12
docker --version             # >=24
tesseract --version          # >=5
```

---

## 1. Clone + Python environment

```bash
cd /path/to/carbonTraceAI_mvp
python3 -m venv .venv
source .venv/bin/activate
pip install --prefer-binary --no-cache-dir -r requirements.txt
```

The `--prefer-binary --no-cache-dir` flags avoid a known wedge where `cryptography` builds from source on slow networks. Total install ~2 minutes on a warm pip cache.

Verify:
```bash
python -m pytest tests/ -q
# expected: 30 passed
```

---

## 2. Smoke-test path (no Docker, ~30 seconds)

Useful for first-time orientation and CI. Seeds the canonical SQLite store directly from Python, runs the calc engine, produces XML + CSV + JSON.

```bash
rm -f data/carbontrace.db data/reports/*
python - <<'PY'
from datetime import date
from src.core.enums import (AluminiumRoute, AnodeType, Country, GwpSet, MeterType,
                            MonitoringMethod, Sector, SourceMethod, UnitOfMeasure,
                            VerificationOpinion)
from src.core.models import (AluminiumProcessRecord, CarbonPricePaid, EnergyConsumption,
                             Facility, MonitoringMeta, PrecursorPurchase, ProductionRun,
                             RECsCertificate)
from src.storage.repository import Repository

qs, qe = date(2026, 4, 1), date(2026, 6, 30)
repo = Repository()

repo.save_many([Facility(
    source=SourceMethod.MANUAL, legal_entity_name="Mozal SA",
    company_registration_number="MZ-100", plant_operating_name="Mozal Smelter",
    physical_address="Beluluane", country=Country.MZ, sector=Sector.ALUMINIUM,
    cn_codes=["76011000"], reporting_period_start=qs, reporting_period_end=qe,
    design_capacity_t_per_year=580_000, functional_currency="USD",
    eori="MZ100123456789", un_locode="MZMPM", cbam_installation_id="MZ-INST-001",
)])
repo.save_many([ProductionRun(
    source=SourceMethod.ERP, facility_id="MOZAL-MZ-01", sector=Sector.ALUMINIUM,
    product_name="primary_aluminium_ingot", product_cn_code="76011000",
    batch_run_id="WO-Q2-001", output_tonnes=50_000,
    eu_export_tonnes=30_000, domestic_sales_tonnes=20_000,
    aluminium_route=AluminiumRoute.PRIMARY, anode_type=AnodeType.PRE_BAKE,
    run_started_at=qs, run_ended_at=qe,
)])
repo.save_many([AluminiumProcessRecord(
    source=SourceMethod.MANUAL, facility_id="MOZAL-MZ-01",
    period_start=qs, period_end=qe,
    anode_consumption_tonnes=21_500, primary_al_output_tonnes=50_000,
    anode_effect_minutes=0.12,
)])
repo.save_many([EnergyConsumption(
    source=SourceMethod.METER, facility_id="MOZAL-MZ-01",
    period_start=qs, period_end=qe,
    meter_type=MeterType.ELECTRICITY_GRID,
    quantity=750_000_000, unit=UnitOfMeasure.KWH, cost_centre="potline_1",
)])
repo.save_many([PrecursorPurchase(
    source=SourceMethod.SUPPLIER, facility_id="MOZAL-MZ-01",
    po_number="PO-Q2-101", precursor_name="alumina",
    precursor_cn_code="28182000", quantity_tonnes=96_000,
    supplier_name="Alunorte", supplier_country="BR",
    embedded_emissions_tco2_per_t=1.05, ee_method="actual", purchase_date=qs,
)])
repo.save_many([CarbonPricePaid(
    source=SourceMethod.MANUAL, facility_id="MOZAL-MZ-01",
    period_start=qs, period_end=qe,
    tax_type="Worked-example carbon tax", gross_emissions_tco2e=10_000,
    net_taxable_tco2e=10_000, rate_local_per_tco2e=20.0, local_currency="EUR",
    total_paid_local=200_000, total_paid_eur=200_000, fx_rate_local_to_eur=1.0,
)])
repo.save_many([RECsCertificate(
    source=SourceMethod.MANUAL, facility_id="MOZAL-MZ-01",
    period_start=qs, period_end=qe,
    certificate_type="I-REC", registry="I-REC Standard",
    certificate_id="IREC-2026-MZ-001", mwh=200_000,
    generation_source="solar", generation_country="MZ", vintage_year=2026,
)])
repo.save_many([MonitoringMeta(
    source=SourceMethod.MANUAL, facility_id="MOZAL-MZ-01",
    period_start=qs, period_end=qe,
    monitoring_method=MonitoringMethod.TIER2,
    emission_factor_source="IPCC 2006 V2 + supplier-actual",
    gwp_set=GwpSet.AR6,
    verifier_name="DNV", verifier_accreditation_id="DNV-CBAM-001",
    verification_opinion=VerificationOpinion.REASONABLE, uncertainty_pct=7.5,
)])
print("seeded")
PY

python -m scripts.run_calculation 2026-Q2
ls -la data/reports/
```

You should see:
```
CBAM run <uuid>
  • MOZAL-MZ-01 [2026-Q2]  total=204,207 tCO2e  CBAM cost=€6,738,840
      ↳ CN 76011000  out=50,000t  SEE=4.084  adj=2.995  ±4.5%  est-share=36.3%
```

This proves the calc engine works without any external dependency. Skip to **§4** if you don't need ERPNext today.

---

## 3. Full path — ERPNext + ingestion + calc

### 3a. Boot ERPNext

```bash
docker compose -f docker-compose.erpnext.yml up -d
```

First boot pulls the `frappe/erpnext:v15` image (~1.5 GB) and runs `new-site` inside the `create-site` container. **Expect 3–5 minutes** before the site responds.

Watch progress:
```bash
docker compose -f docker-compose.erpnext.yml logs -f create-site
```

When you see `Installing erpnext... done`, hit:
```
http://localhost:8080
# Login: Administrator / admin
```

You should land on the ERPNext desk. Empty until you seed.

### 3b. Seed a factory profile

```bash
python -m scripts.seed_erpnext --profile mozal_aluminium
# or:
python -m scripts.seed_erpnext --profile ocp_fertiliser
```

The script logs in with Administrator/admin, generates an API key + secret, writes them to `.env.erpnext` (chmod 600), then injects:

- ~21 Custom Fields
- 5 UOMs, 4 Item Groups
- 10 Items, 7–9 Suppliers, 5 EU Customers, 5 Cost Centres
- 2–4 BOMs
- ~1,440 Work Orders (incl. ~18 rework + ~6 scrap)
- ~960 stoichiometrically-sized Purchase Orders
- ~575 Purchase Invoices (linked to POs)
- ~1,430 Stock Entries
- ~1,440 Quality Inspections
- ~144 (Mozal) / ~288 (OCP) Sales Invoices

End-to-end seeding time: **10–25 minutes** depending on Docker host speed. Output:

```
[seed:mozal_aluminium] items=10 suppliers=10 customers=5 cost_centres=5 boms=2
                       wo=1442 rework=18 po=956 pinv=574 stock=1380 qa=1442
                       sinv=144 errors=0
```

Browse the result at http://localhost:8080 — every doctype is populated with real records.

> **Tip — shrink the seed for fast demos**: pass `--months 3 --work-orders-per-month 12 --purchase-orders-per-month 8` to drop the run to ~2 minutes total. Numbers in the calc engine scale linearly so the SEE outputs still look correct.

### 3c. Pull ERPNext → canonical store → manual/supplier/OCR

```bash
python -m scripts.run_erpnext_pipeline --facility-id MOZAL-MZ-01
```

The script:
1. Loads ERPNext creds from `.env.erpnext`
2. Runs `ERPNextRunner.sync_all()` → writes JSONL to `data/raw/erpnext/<stream>/<ts>.jsonl`
3. `ErpIngestor` maps each stream to canonical Pydantic models → SQLite
4. Adds 1 manual facility, 1 manual sensor reading, 1 supplier-portal precursor declaration
5. OCRs the sample electricity invoice at `data/samples/sample_electricity_invoice.png`

Expected output:
```
[SourceMethod.ERP/production_runs]   in=1442 ok=1442 err=0
[SourceMethod.ERP/purchase_orders]   in=956  ok=956  err=0
[SourceMethod.ERP/bill_of_materials] in=8    ok=8    err=0
[SourceMethod.ERP/invoices]          in=574  ok=574  err=0
[SourceMethod.MANUAL/facility]       in=1    ok=1    err=0
[SourceMethod.METER/sensor_reading_manual] in=1 ok=1 err=0
[SourceMethod.SUPPLIER/supplier_portal_submission] in=1 ok=1 err=0
[SourceMethod.INVOICE/ocr_invoices]  in=1    ok=1    err=0
TOTAL  in=2984 ok=2984 err=0
```

### 3d. Run the CBAM calc engine

```bash
python -m scripts.run_calculation 2026-Q2
# Or auto-pick the latest quarter:
python -m scripts.run_calculation
```

Produces `data/reports/cbam_quarterly_<run_id>.xml`, `.csv`, and `dashboard_<run_id>.json`. See [01_OUTPUTS.md](01_OUTPUTS.md) for content samples.

---

## 4. Remote-demo path (cloud Airbyte or external pitch)

Expose your local ERPNext over HTTPS for an external Airbyte or pitch audience:

```bash
ngrok http 8080
```

You'll get an HTTPS URL like `https://a1b2c3.ngrok.io`. Use it as the `base_url`:

```bash
python -m scripts.onboard_client \
  --connector erpnext_direct \
  --facility-id MOZAL-MZ-01 \
  --base-url https://a1b2c3.ngrok.io \
  --api-key   <from .env.erpnext> \
  --api-secret <from .env.erpnext>
```

The framework saves the connection (Fernet-encrypted creds), provisions an Airbyte source if you've configured one, and syncs.

For the **Airbyte ERPNext path** specifically: deploy Airbyte (Cloud or Docker), set `AIRBYTE_API_URL` in your env, then pick `--connector erpnext_airbyte` in `onboard_client`. The `AirbyteProvisioner` creates source + destination + connection idempotently.

---

## 5. Running the test suite

```bash
python -m pytest tests/ -q -W "ignore::DeprecationWarning"
# 30 tests pass in ~1.5 seconds
```

Tests cover:
- IPCC defaults, CBAM Annex defaults, AR5/AR6 GWPs
- Estimators with measured > IPCC fallback
- EF priority resolution
- Uncertainty quadrature
- Every formula branch (fuel / process / electricity / steam / precursor)
- Adjusted SEE with carbon-price deduction
- REC offset on indirect emissions
- Full engine run on aluminium facility
- XML / CSV / dashboard-JSON renderer schema
- Coproduct allocation
- ERPNext client iter_all pagination (mocked)
- ERPNext runner JSONL writer
- ErpIngestor consuming ERPNext output
- Manual / sensor / supplier ingestors
- OCR invoice parser
- Connector registry + onboarding factory
- Credential vault round-trip
- Connector-unreachable error branch

---

## 6. Environment variables

Set in `.env` (auto-loaded by `python-dotenv`) or your shell:

| Var | Default | Purpose |
|---|---|---|
| `CARBONTRACE_DB_URL` | `sqlite:///data/carbontrace.db` | Canonical store URL (Postgres works too) |
| `CARBONTRACE_VAULT_KEY` | auto-generated dev key at `data/.vault.key` | Fernet key for the credential vault. **Set explicitly in production.** |
| `CARBONTRACE_DATA_DIR` | `./data` | Where raw landings + reports go |
| `ERPNEXT_BASE_URL` | (written by seed) | ERPNext URL |
| `ERPNEXT_API_KEY` / `ERPNEXT_API_SECRET` | (written by seed) | Frappe API token pair |
| `AIRBYTE_API_URL` | `http://localhost:8000/api/v1` | Airbyte API base for the provisioner |
| `AIRBYTE_USERNAME` / `AIRBYTE_PASSWORD` | (none) | Basic auth if Airbyte requires it |

---

## 7. Troubleshooting

### ERPNext won't come up

```bash
docker compose -f docker-compose.erpnext.yml logs frontend
docker compose -f docker-compose.erpnext.yml logs create-site
```

Common causes:
- **Port 8080 already in use** — change the `ports:` map in `docker-compose.erpnext.yml`
- **MariaDB took too long to come up** — the `create-site` container has a 120s wait built in. Retry: `docker compose down && docker compose up -d`.
- **Architecture mismatch on Apple Silicon** — the official `frappe/erpnext:v15` image is multi-arch; if you see "exec format error" run `docker pull --platform linux/arm64 frappe/erpnext:v15.74.4`.

### `Tesseract not found` during OCR

```bash
# macOS
brew install tesseract

# Linux
sudo apt install tesseract-ocr

# verify
which tesseract
tesseract --version
```

### Seed script fails partway through

Re-run it — the seeder is idempotent on masters (Items, Suppliers, BOMs are upserted) and purely additive on transactional docs. You'll get duplicated Work Orders if you re-seed without `docker compose down -v` first; that's fine for demos.

To wipe and start over:
```bash
docker compose -f docker-compose.erpnext.yml down -v
rm -f .env.erpnext data/carbontrace.db
docker compose -f docker-compose.erpnext.yml up -d
# wait, then re-seed
```

### `pip install` wedges

```bash
pip install --prefer-binary --no-cache-dir -r requirements.txt
```

The `--prefer-binary` flag forces wheel use over source builds (the source build for `cryptography` is what historically hangs on slow networks).

### Calc engine reports `output_tonnes <= 0`

Means no `production_runs` rows landed in the canonical store for the requested quarter. Check:
```bash
sqlite3 data/carbontrace.db "SELECT facility_id, COUNT(*) FROM production_runs;"
```
If zero, re-run `scripts.run_erpnext_pipeline`.

### Calc engine flags `>20% estimated emissions`

That's not an error — it's the verifier flag per CBAM IR Art.4(3). To reduce it: provide measured NCV / CC / OF for fuels (manual sensor form), supplier-actual EE for precursors (supplier portal form), or supplier-specific grid EF (market-based) in the manual sensor form.

---

## 8. One-liner cheatsheet

```bash
# fresh checkout to verified report
python3 -m venv .venv && source .venv/bin/activate
pip install --prefer-binary --no-cache-dir -r requirements.txt
python -m pytest tests/ -q                                    # 30 passed
docker compose -f docker-compose.erpnext.yml up -d            # wait 3-5 min
python -m scripts.seed_erpnext --profile mozal_aluminium      # 10-25 min
python -m scripts.run_erpnext_pipeline                        # ~30 sec
python -m scripts.run_calculation 2026-Q2                     # ~1 sec
ls -la data/reports/                                          # 3 artefacts
```

---

## 9. What to read next

→ [03_ROADMAP.md](03_ROADMAP.md) — the gaps, the calc-engine hardening list, the Next.js + Tremor dashboard build, the FastAPI / Postgres productionisation path, and sector expansion (steel / hydrogen / cement).
