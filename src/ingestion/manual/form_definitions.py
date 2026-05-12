"""Declarative form definitions for the manual-entry layer.

Each form is the contract between the future web UI and the ManualIngestor.
A form lists its fields, types, units, validation rules, and which canonical
model the submission maps to. The web team can render any form straight from
this dict — no hand-coded forms.
"""
from __future__ import annotations

from typing import Any


FORMS: dict[str, dict[str, Any]] = {
    # ---- Block A — facility ----
    "facility": {
        "title": "Facility & Legal Identity",
        "block": "A",
        "model": "Facility",
        "cadence": "annual",
        "fields": [
            {"name": "legal_entity_name",          "label": "Legal entity name",         "type": "string", "required": True},
            {"name": "company_registration_number","label": "Company registration #",     "type": "string", "required": True},
            {"name": "plant_operating_name",       "label": "Plant operating name",       "type": "string", "required": True},
            {"name": "physical_address",           "label": "Physical address",           "type": "string", "required": True},
            {"name": "gps_lat",                    "label": "GPS latitude",               "type": "number"},
            {"name": "gps_lon",                    "label": "GPS longitude",              "type": "number"},
            {"name": "country",                    "label": "Country",                    "type": "enum", "options": ["MZ","ZA","MA","EG"], "required": True},
            {"name": "sector",                     "label": "Sector",                     "type": "enum", "options": ["aluminium","fertiliser"], "required": True},
            {"name": "eu_cbam_declarant_name",     "label": "EU CBAM declarant",          "type": "string"},
            {"name": "cn_codes",                   "label": "CN codes (comma-separated)", "type": "list[string]"},
            {"name": "nace_code",                  "label": "NACE code",                  "type": "string"},
            {"name": "reporting_period_start",     "label": "Reporting period start",     "type": "date", "required": True},
            {"name": "reporting_period_end",       "label": "Reporting period end",       "type": "date", "required": True},
            {"name": "design_capacity_t_per_year", "label": "Design capacity (t/yr)",     "type": "number"},
            {"name": "functional_currency",        "label": "Currency",                   "type": "enum", "options": ["ZAR","MZN","MAD","EGP","EUR","USD"]},
            # CBAM Section 1 + 3 additions
            {"name": "eori",                       "label": "EORI",                       "type": "string"},
            {"name": "un_locode",                  "label": "UN/LOCODE",                  "type": "string", "placeholder": "MZMPM"},
            {"name": "cbam_installation_id",       "label": "CBAM installation ID (EU registry)", "type": "string"},
            {"name": "jv_partners",                "label": "JV partners",                "type": "list[object]"},
            {"name": "process_diagram_path",       "label": "Process diagram (PDF)",      "type": "file"},
        ],
    },

    # ---- Block D2 — aluminium process (manual sensor entry until SCADA online) ----
    "aluminium_process_monthly": {
        "title": "Monthly Aluminium Process Data",
        "block": "D2",
        "model": "AluminiumProcessRecord",
        "cadence": "monthly",
        "applies_to": ["aluminium"],
        "fields": [
            {"name": "facility_id",               "type": "string", "required": True},
            {"name": "period_start",              "type": "date",   "required": True},
            {"name": "period_end",                "type": "date",   "required": True},
            {"name": "alumina_consumed_tonnes",   "type": "number", "unit": "tonnes"},
            {"name": "anode_consumption_tonnes",  "type": "number", "unit": "tonnes"},
            {"name": "anode_effect_per_pot_day",  "type": "number", "unit": "events/pot/day"},
            {"name": "anode_effect_minutes",      "type": "number", "unit": "minutes"},
            {"name": "alf3_kg_per_t_al",          "type": "number", "unit": "kg/t Al"},
            {"name": "primary_al_output_tonnes",  "type": "number", "unit": "tonnes"},
            {"name": "secondary_al_output_tonnes","type": "number", "unit": "tonnes"},
            {"name": "scrap_al_input_tonnes",     "type": "number", "unit": "tonnes"},
        ],
    },

    # ---- Block D3 — fertiliser process ----
    "fertiliser_process_monthly": {
        "title": "Monthly Fertiliser Process Data",
        "block": "D3",
        "model": "FertiliserProcessRecord",
        "cadence": "monthly",
        "applies_to": ["fertiliser"],
        "fields": [
            {"name": "facility_id",                    "type": "string", "required": True},
            {"name": "period_start",                   "type": "date",   "required": True},
            {"name": "period_end",                     "type": "date",   "required": True},
            {"name": "feedstock_natural_gas_nm3",      "type": "number", "unit": "Nm3"},
            {"name": "ammonia_production_tonnes",      "type": "number", "unit": "tonnes"},
            {"name": "co2_captured_tco2",              "type": "number", "unit": "tCO2"},
            {"name": "co2_used_in_urea_tco2",          "type": "number", "unit": "tCO2"},
            {"name": "urea_production_tonnes",         "type": "number", "unit": "tonnes"},
            {"name": "nitric_acid_production_tonnes",  "type": "number", "unit": "tonnes"},
            {"name": "n2o_destruction_efficiency_pct", "type": "number", "unit": "%"},
            {"name": "n2o_kg_per_t_hno3",              "type": "number", "unit": "kg/t HNO3"},
        ],
    },

    # ---- Manual sensor reading (when no SCADA pull is wired) ----
    "sensor_reading_manual": {
        "title": "Manual Sensor / Meter Reading",
        "block": "C/D",
        "model": "EnergyConsumption",
        "cadence": "ad_hoc",
        "fields": [
            {"name": "facility_id",  "type": "string", "required": True},
            {"name": "period_start", "type": "date",   "required": True},
            {"name": "period_end",   "type": "date",   "required": True},
            {"name": "meter_id",     "type": "string"},
            {"name": "meter_type",   "type": "enum", "options": [
                "electricity_grid","electricity_subprocess","natural_gas","steam",
                "solar_pv","diesel_generator","anode_effect","stack_n2o"], "required": True},
            {"name": "cost_centre",  "type": "string"},
            {"name": "quantity",     "type": "number", "required": True},
            {"name": "unit",         "type": "enum", "options": ["kWh","Nm3","GJ","litres","tonnes","kg","events_per_pot_day","kg_per_t"], "required": True},
            {"name": "quality_flag", "type": "enum", "options": ["ok","estimated","calibration_due","missing"], "default": "ok"},
        ],
    },

    # ---- Block E — supplier portal submission ----
    "supplier_portal_submission": {
        "title": "Supplier Embedded Emissions Declaration",
        "block": "E",
        "model": "PrecursorPurchase",
        "cadence": "annual",
        "fields": [
            {"name": "facility_id",                   "type": "string", "required": True},
            {"name": "po_number",                     "type": "string"},
            {"name": "precursor_name",                "type": "string", "required": True},
            {"name": "precursor_cn_code",             "type": "string", "required": True},
            {"name": "quantity_tonnes",               "type": "number", "required": True},
            {"name": "supplier_name",                 "type": "string", "required": True},
            {"name": "supplier_country",              "type": "string", "required": True},
            {"name": "supplier_installation_id",      "type": "string"},
            {"name": "embedded_emissions_tco2_per_t", "type": "number", "unit": "tCO2e/t", "required": True},
            {"name": "ee_method",                     "type": "enum", "options": ["actual","default"], "default": "actual"},
            {"name": "verification_cert_path",        "type": "file"},
            {"name": "supplier_carbon_price_eur",     "type": "number", "unit": "EUR/tCO2e"},
            {"name": "scrap_recycled_pct",            "type": "number", "unit": "%"},
            {"name": "purchase_date",                 "type": "date",   "required": True},
        ],
    },

    # ---- Block F — fugitive (manual annual top-up form) ----
    "fugitive_annual": {
        "title": "Annual Fugitive Emissions",
        "block": "F",
        "model": "FugitiveEmission",
        "cadence": "annual",
        "fields": [
            {"name": "facility_id",          "type": "string", "required": True},
            {"name": "period_start",         "type": "date",   "required": True},
            {"name": "period_end",           "type": "date",   "required": True},
            {"name": "refrigerant_type",     "type": "string"},
            {"name": "refrigerant_topup_kg", "type": "number", "unit": "kg"},
            {"name": "sf6_charge_kg",        "type": "number", "unit": "kg"},
            {"name": "sf6_topup_kg",         "type": "number", "unit": "kg"},
            {"name": "flaring_nm3",          "type": "number", "unit": "Nm3"},
        ],
    },

    # ---- Block K — monitoring / verification ----
    "monitoring_meta": {
        "title": "Monitoring & Verification",
        "block": "K",
        "model": "MonitoringMeta",
        "cadence": "per_period",
        "fields": [
            {"name": "facility_id",                "type": "string", "required": True},
            {"name": "period_start",               "type": "date",   "required": True},
            {"name": "period_end",                 "type": "date",   "required": True},
            {"name": "monitoring_method",          "type": "enum", "options": ["tier1","tier2","tier3","cems","mass_balance"], "required": True},
            {"name": "emission_factor_source",     "type": "string", "required": True},
            {"name": "gwp_set",                    "type": "enum", "options": ["AR5","AR6"], "required": True},
            {"name": "meter_id",                   "type": "string"},
            {"name": "last_calibration_date",      "type": "date"},
            {"name": "verifier_name",              "type": "string"},
            {"name": "verifier_accreditation_id",  "type": "string"},
            {"name": "verification_opinion",       "type": "enum", "options": ["reasonable","limited","qualified","adverse","not_verified"]},
            {"name": "verification_report_path",   "type": "file"},
            {"name": "sampling_frequency",         "type": "enum", "options": ["continuous","daily","weekly","per_batch","monthly","quarterly","annual"]},
            {"name": "uncertainty_pct",            "type": "number", "unit": "%"},
            {"name": "material_misstatements",     "type": "list[object]"},
            {"name": "notes",                      "type": "string"},
        ],
    },

    # ---- Section 4 — Process boundary ----
    "process_boundary": {
        "title": "Process Boundary Description",
        "block": "4",
        "model": "ProcessBoundary",
        "cadence": "annual",
        "fields": [
            {"name": "facility_id",                "type": "string", "required": True},
            {"name": "product_cn_code",            "type": "string", "required": True},
            {"name": "aggregated_goods_category",  "type": "string", "required": True},
            {"name": "boundary_description",       "type": "text",   "required": True},
            {"name": "included_unit_processes",    "type": "list[string]"},
            {"name": "excluded_unit_processes",    "type": "list[string]"},
            {"name": "process_diagram_path",       "type": "file"},
            {"name": "effective_from",             "type": "date",   "required": True},
            {"name": "effective_to",               "type": "date"},
        ],
    },

    # ---- Section 6 — RECs / GOs ----
    "recs_certificate": {
        "title": "REC / Guarantee of Origin",
        "block": "6",
        "model": "RECsCertificate",
        "cadence": "per_certificate",
        "fields": [
            {"name": "facility_id",       "type": "string", "required": True},
            {"name": "period_start",      "type": "date",   "required": True},
            {"name": "period_end",        "type": "date",   "required": True},
            {"name": "certificate_type",  "type": "enum",   "options": ["REC","GO","I-REC"], "required": True},
            {"name": "registry",          "type": "string", "required": True},
            {"name": "certificate_id",    "type": "string", "required": True},
            {"name": "mwh",               "type": "number", "required": True},
            {"name": "generation_source", "type": "enum", "options": ["solar","wind","hydro","nuclear","geothermal","biomass"]},
            {"name": "generation_country","type": "string"},
            {"name": "vintage_year",      "type": "number"},
            {"name": "retired",           "type": "boolean", "default": True},
            {"name": "document_path",     "type": "file"},
        ],
    },

    # ---- Section 6 — CHP ----
    "chp_record": {
        "title": "CHP Output (electrical + thermal)",
        "block": "6",
        "model": "CHPRecord",
        "cadence": "monthly",
        "fields": [
            {"name": "facility_id",            "type": "string", "required": True},
            {"name": "period_start",           "type": "date",   "required": True},
            {"name": "period_end",             "type": "date",   "required": True},
            {"name": "electrical_output_kwh",  "type": "number", "unit": "kWh"},
            {"name": "thermal_output_gj",      "type": "number", "unit": "GJ"},
            {"name": "fuel_input_gj",          "type": "number", "unit": "GJ"},
            {"name": "fuel_type",              "type": "enum", "options": ["natural_gas","diesel","heavy_fuel_oil","lpg","coal","coke","biomass"]},
            {"name": "overall_efficiency_pct", "type": "number", "unit": "%"},
        ],
    },

    # ---- Section 8 / Block G — Carbon price paid ----
    "carbon_price_paid": {
        "title": "Carbon Price Paid (Country of Origin)",
        "block": "G",
        "model": "CarbonPricePaid",
        "cadence": "per_period",
        "fields": [
            {"name": "facility_id",              "type": "string", "required": True},
            {"name": "period_start",             "type": "date",   "required": True},
            {"name": "period_end",               "type": "date",   "required": True},
            {"name": "tax_type",                 "type": "string", "required": True, "placeholder": "SA Carbon Tax Act 15/2019"},
            {"name": "tax_legislation_ref",      "type": "string"},
            {"name": "gross_emissions_tco2e",    "type": "number", "required": True, "unit": "tCO2e"},
            {"name": "tax_free_allowances_pct",  "type": "number", "unit": "%"},
            {"name": "net_taxable_tco2e",        "type": "number", "required": True, "unit": "tCO2e"},
            {"name": "rate_local_per_tco2e",     "type": "number", "required": True},
            {"name": "local_currency",           "type": "enum",   "options": ["ZAR","MZN","MAD","EGP","EUR","USD"], "required": True},
            {"name": "total_paid_local",         "type": "number", "required": True},
            {"name": "total_paid_eur",           "type": "number", "required": True, "unit": "EUR"},
            {"name": "fx_rate_local_to_eur",     "type": "number", "required": True},
            {"name": "payment_receipt_path",     "type": "file"},
            {"name": "free_allocation_tco2e",    "type": "number", "unit": "tCO2e"},
        ],
    },

    # ---- Section 9 — MR plan ----
    "mr_plan": {
        "title": "Monitoring & Reporting Plan",
        "block": "K",
        "model": "MRPlan",
        "cadence": "annual",
        "fields": [
            {"name": "facility_id",             "type": "string", "required": True},
            {"name": "plan_version",            "type": "string", "required": True},
            {"name": "effective_from",          "type": "date",   "required": True},
            {"name": "effective_to",            "type": "date"},
            {"name": "approved_by",             "type": "string"},
            {"name": "plan_document_path",      "type": "file"},
            {"name": "summary",                 "type": "text"},
            {"name": "covered_emission_sources","type": "list[string]"},
        ],
    },

    # ---- Cost-centre allocation (Block C2.2) ----
    "cost_centre_allocation": {
        "title": "Cost-Centre Electricity / Steam Allocation",
        "block": "C",
        "model": "CostCentreAllocation",
        "cadence": "monthly",
        "fields": [
            {"name": "facility_id",        "type": "string", "required": True},
            {"name": "period_start",       "type": "date",   "required": True},
            {"name": "period_end",         "type": "date",   "required": True},
            {"name": "cost_centre",        "type": "string", "required": True},
            {"name": "cost_centre_id",     "type": "string"},
            {"name": "parent_cost_centre", "type": "string"},
            {"name": "allocated_kwh",      "type": "number", "unit": "kWh"},
            {"name": "allocated_steam_gj", "type": "number", "unit": "GJ"},
            {"name": "allocation_basis",   "type": "enum", "options": ["mass","energy","economic","none"]},
            {"name": "notes",              "type": "string"},
        ],
    },
}


def get_form(form_id: str) -> dict[str, Any]:
    if form_id not in FORMS:
        raise KeyError(f"Unknown form {form_id!r}. Known: {list(FORMS)}")
    return FORMS[form_id]
