"""End-to-end pipeline: pull ERPNext via REST → canonical store → manual +
supplier + OCR layers on top.

Picks up ERPNext creds from `.env.erpnext` (written by `seed_erpnext.py`)
or the corresponding env vars.
"""
from __future__ import annotations

import argparse
import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from src.ingestion.erp.erpnext_client import ERPNextCredentials
from src.ingestion.orchestrator import IngestionOrchestrator

load_dotenv(".env.erpnext", override=False)


def main() -> int:
    p = argparse.ArgumentParser(description="Run the full carbonTraceAI pipeline against ERPNext.")
    p.add_argument("--base-url",   default=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8080"))
    p.add_argument("--api-key",    default=os.getenv("ERPNEXT_API_KEY"))
    p.add_argument("--api-secret", default=os.getenv("ERPNEXT_API_SECRET"))
    p.add_argument("--facility-id", default="MOZAL-MZ-01",
                   help="Facility ID for manual + OCR rows.")
    p.add_argument("--skip-ocr", action="store_true")
    args = p.parse_args()

    if not (args.api_key and args.api_secret):
        raise SystemExit(
            "ERPNext API key/secret not set. Run `python -m scripts.seed_erpnext` first "
            "or export ERPNEXT_API_KEY and ERPNEXT_API_SECRET."
        )

    orch = IngestionOrchestrator()

    # 1. ERPNext — every CBAM-relevant stream
    orch.run_erpnext_direct(ERPNextCredentials(
        base_url=args.base_url, api_key=args.api_key, api_secret=args.api_secret,
    ))

    # 2. Facility onboarding (manual)
    orch.run_manual("facility", [{
        "legal_entity_name": "Mozal SA",
        "company_registration_number": "MZ-100123",
        "plant_operating_name": "Mozal Aluminium Smelter",
        "physical_address": "Beluluane Industrial Park, Boane",
        "gps_lat": -25.973, "gps_lon": 32.474,
        "country": "MZ", "sector": "aluminium",
        "eu_cbam_declarant_name": "EU Importer GmbH",
        "cn_codes": ["76011000"],
        "reporting_period_start": date(2026, 1, 1),
        "reporting_period_end":   date(2026, 12, 31),
        "design_capacity_t_per_year": 580_000,
        "functional_currency": "USD",
    }])

    # 3. Manual sensor / meter reading — MVP has no SCADA
    orch.run_sensor([{
        "facility_id": args.facility_id,
        "period_start": date(2026, 4, 1),
        "period_end":   date(2026, 4, 30),
        "meter_id": "MTR-PL1-0001",
        "meter_type": "electricity_subprocess",
        "cost_centre": "potline_1",
        "quantity": 690_000_000, "unit": "kWh",
        "quality_flag": "ok",
    }])

    # 4. Supplier portal — actual embedded emissions for alumina
    orch.run_supplier([{
        "facility_id": args.facility_id,
        "po_number": "PO-DEMO-001",
        "precursor_name": "alumina",
        "precursor_cn_code": "28182000",
        "quantity_tonnes": 25_000,
        "supplier_name": "Alunorte Refinery",
        "supplier_country": "BR",
        "embedded_emissions_tco2_per_t": 1.05,
        "ee_method": "actual",
        "purchase_date": date(2026, 3, 1),
    }])

    # 5. OCR — sample electricity invoice (synthesised on first run)
    if not args.skip_ocr:
        sample = Path("data/samples/sample_electricity_invoice.png")
        if sample.exists():
            orch.run_ocr([sample], facility_id=args.facility_id)

    print(orch.report.summary())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
