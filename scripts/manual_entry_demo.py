"""Manual entry demo — submits one example payload per form.

Demonstrates the manual + sensor + supplier-portal paths feeding the same
canonical store the ERP path writes to.
"""
from __future__ import annotations

from datetime import date

from src.ingestion.orchestrator import IngestionOrchestrator


def main() -> int:
    orch = IngestionOrchestrator()

    # Block A — facility (manual)
    orch.run_manual("facility", [
        {
            "legal_entity_name": "Mozal SA",
            "company_registration_number": "MZ-100123",
            "plant_operating_name": "Mozal Aluminium Smelter",
            "physical_address": "Beluluane Industrial Park, Boane",
            "gps_lat": -25.973, "gps_lon": 32.474,
            "country": "MZ", "sector": "aluminium",
            "eu_cbam_declarant_name": "EU Importer GmbH",
            "cn_codes": ["76011000"],
            "nace_code": "24.42",
            "reporting_period_start": date(2026, 1, 1),
            "reporting_period_end": date(2026, 12, 31),
            "design_capacity_t_per_year": 580000,
            "functional_currency": "USD",
        }
    ])

    # Block D2 — aluminium process (manual)
    orch.run_manual("aluminium_process_monthly", [
        {
            "facility_id": "MOZAL-MZ-01",
            "period_start": date(2026, 4, 1),
            "period_end":   date(2026, 4, 30),
            "alumina_consumed_tonnes": 96000,
            "anode_consumption_tonnes": 22500,
            "anode_effect_per_pot_day": 0.08,
            "anode_effect_minutes": 1.2,
            "alf3_kg_per_t_al": 18,
            "primary_al_output_tonnes": 48000,
            "secondary_al_output_tonnes": 0,
            "scrap_al_input_tonnes": 0,
        }
    ])

    # Block C — manual sensor reading
    orch.run_sensor([
        {
            "facility_id": "MOZAL-MZ-01",
            "period_start": date(2026, 4, 1),
            "period_end":   date(2026, 4, 30),
            "meter_id": "MTR-PL1-0001",
            "meter_type": "electricity_subprocess",
            "cost_centre": "potline_1",
            "quantity": 690_000_000,
            "unit": "kWh",
            "quality_flag": "ok",
        }
    ])

    # Block E — supplier portal submission
    orch.run_supplier([
        {
            "facility_id": "MOZAL-MZ-01",
            "po_number": "PO-100456",
            "precursor_name": "alumina",
            "precursor_cn_code": "28182000",
            "quantity_tonnes": 12000,
            "supplier_name": "Alunorte",
            "supplier_country": "BR",
            "supplier_installation_id": "BR-ALN-01",
            "embedded_emissions_tco2_per_t": 1.05,
            "ee_method": "actual",
            "supplier_carbon_price_eur": 0.0,
            "scrap_recycled_pct": 0,
            "purchase_date": date(2026, 3, 15),
        }
    ])

    print(orch.report.summary())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
