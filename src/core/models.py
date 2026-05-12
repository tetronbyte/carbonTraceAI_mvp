"""Canonical Pydantic models — every ingestion source produces these.

Field codes (A1, B1.1, ...) trace back to the CBAM data map for auditability.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Any, Optional


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import (
    AllocationMethod,
    AluminiumRoute,
    AmmoniaRoute,
    AnodeType,
    Country,
    EFTier,
    FuelType,
    GwpSet,
    MeterType,
    MonitoringMethod,
    SamplingFrequency,
    Sector,
    SourceMethod,
    UnitOfMeasure,
    VerificationOpinion,
    WorkOrderOutcome,
)


def _new_id() -> str:
    return str(uuid.uuid4())


class CarbonModel(BaseModel):
    """Base config — every canonical record is auditable."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )

    id: str = Field(default_factory=_new_id)
    source: SourceMethod
    ingested_at: datetime = Field(default_factory=_utcnow)
    raw_ref: Optional[str] = Field(
        default=None,
        description="Pointer to raw landing payload (file path, line offset, doc id).",
    )


# -------- BLOCK A — facility --------
class Facility(CarbonModel):
    legal_entity_name: str
    company_registration_number: str
    plant_operating_name: str
    physical_address: str
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    country: Country
    sector: Sector
    eu_cbam_declarant_name: Optional[str] = None
    cn_codes: list[str] = Field(default_factory=list)
    nace_code: Optional[str] = None
    reporting_period_start: date
    reporting_period_end: date
    design_capacity_t_per_year: Optional[float] = None
    functional_currency: str = "EUR"
    # ---- CBAM section 1 + 3 additions ----
    eori: Optional[str] = None                           # EU Economic Operator ID
    un_locode: Optional[str] = None                      # e.g. MZMPM (Maputo)
    cbam_installation_id: Optional[str] = None           # EU registry ID once issued
    jv_partners: list[dict[str, Any]] = Field(default_factory=list)  # [{"name", "equity_pct"}]
    process_diagram_path: Optional[str] = None           # link to process flow PDF

    @field_validator("cn_codes")
    @classmethod
    def _strip_cn(cls, v: list[str]) -> list[str]:
        return [c.strip().replace(" ", "") for c in v]


# -------- BLOCK B — production --------
class ProductionRun(CarbonModel):
    facility_id: str
    sector: Sector
    product_name: str
    product_cn_code: str
    batch_run_id: str
    output_tonnes: float = Field(ge=0)
    eu_export_tonnes: float = Field(default=0, ge=0)
    domestic_sales_tonnes: float = Field(default=0, ge=0)
    coproduct_tonnes: float = Field(default=0, ge=0)
    scrap_rate_pct: float = Field(default=0, ge=0, le=100)
    aluminium_route: Optional[AluminiumRoute] = None
    anode_type: Optional[AnodeType] = None
    ammonia_route: Optional[AmmoniaRoute] = None
    bom_lines: list[dict[str, Any]] = Field(default_factory=list)
    run_started_at: datetime
    run_ended_at: Optional[datetime] = None
    # ---- CBAM allocation + quality additions ----
    coproduct_allocation_method: AllocationMethod = AllocationMethod.NONE
    allocation_basis: dict[str, float] = Field(default_factory=dict)  # {product: weight}
    coproduct_tonnes_map: dict[str, float] = Field(default_factory=dict)  # {coproduct_cn: tonnes}
    outcome: WorkOrderOutcome = WorkOrderOutcome.COMPLETED
    parent_run_id: Optional[str] = None                  # set when this is a rework of another run


# -------- BLOCK C — energy --------
class EnergyConsumption(CarbonModel):
    facility_id: str
    period_start: date
    period_end: date
    meter_type: MeterType
    meter_id: Optional[str] = None
    cost_centre: Optional[str] = None
    quantity: float = Field(ge=0)
    unit: UnitOfMeasure
    fuel_type: Optional[FuelType] = None
    supplier_name: Optional[str] = None
    ncv_gj_per_tonne: Optional[float] = None
    carbon_content_pct: Optional[float] = None
    oxidation_factor: Optional[float] = None
    grid_emission_factor_kgco2_per_kwh: Optional[float] = None
    quality_flag: str = "ok"


# -------- BLOCK D2 — aluminium process --------
class AluminiumProcessRecord(CarbonModel):
    facility_id: str
    period_start: date
    period_end: date
    alumina_consumed_tonnes: float = Field(default=0, ge=0)            # D2.1
    anode_consumption_tonnes: float = Field(default=0, ge=0)           # D2.2
    soderberg_paste_tonnes: float = Field(default=0, ge=0)             # D2.3
    anode_effect_per_pot_day: float = Field(default=0, ge=0)           # D2.4
    anode_effect_minutes: float = Field(default=0, ge=0)               # D2.5
    cf4_kg_per_t_al: Optional[float] = None                            # D2.6
    c2f6_kg_per_t_al: Optional[float] = None                           # D2.7
    alf3_kg_per_t_al: float = Field(default=0, ge=0)                   # D2.8
    primary_al_output_tonnes: float = Field(default=0, ge=0)           # D2.9
    secondary_al_output_tonnes: float = Field(default=0, ge=0)         # D2.10
    scrap_al_input_tonnes: float = Field(default=0, ge=0)              # D2.11


# -------- BLOCK D3 — fertiliser process --------
class FertiliserProcessRecord(CarbonModel):
    facility_id: str
    period_start: date
    period_end: date
    feedstock_natural_gas_nm3: float = Field(default=0, ge=0)          # D3.1
    ammonia_production_tonnes: float = Field(default=0, ge=0)          # D3.2
    co2_captured_tco2: float = Field(default=0, ge=0)                  # D3.3
    co2_used_in_urea_tco2: float = Field(default=0, ge=0)              # D3.4
    urea_production_tonnes: float = Field(default=0, ge=0)             # D3.5
    nitric_acid_production_tonnes: float = Field(default=0, ge=0)      # D3.6
    n2o_abatement_catalyst: Optional[str] = None                       # D3.7
    n2o_destruction_efficiency_pct: Optional[float] = Field(default=None, ge=0, le=100)  # D3.8
    n2o_kg_per_t_hno3: Optional[float] = None                          # D3.9
    phosphoric_acid_tonnes: float = Field(default=0, ge=0)             # D3.10
    sulphuric_acid_tonnes: float = Field(default=0, ge=0)              # D3.11


# -------- BLOCK E — precursor / supplier --------
class PrecursorPurchase(CarbonModel):
    facility_id: str
    po_number: Optional[str] = None
    precursor_name: str                                                 # E1
    precursor_cn_code: str                                              # E2
    quantity_tonnes: float = Field(ge=0)                                # E3
    supplier_name: str                                                  # E4
    supplier_country: Optional[str] = None                              # E5
    supplier_installation_id: Optional[str] = None                      # E6
    embedded_emissions_tco2_per_t: Optional[float] = Field(default=None, ge=0)  # E7
    ee_method: str = "default"                                          # E8 (actual|default)
    verification_cert_path: Optional[str] = None                        # E9
    cbam_default_value: Optional[float] = None                          # E10
    supplier_carbon_price_eur: Optional[float] = None                   # E11
    scrap_recycled_pct: Optional[float] = Field(default=None, ge=0, le=100)  # E12
    purchase_date: date


# -------- BLOCK F — fugitive --------
class FugitiveEmission(CarbonModel):
    facility_id: str
    period_start: date
    period_end: date
    refrigerant_type: Optional[str] = None
    refrigerant_topup_kg: float = Field(default=0, ge=0)
    sf6_charge_kg: float = Field(default=0, ge=0)
    sf6_topup_kg: float = Field(default=0, ge=0)
    flaring_nm3: float = Field(default=0, ge=0)
    flare_gas_ch4_pct: Optional[float] = Field(default=None, ge=0, le=100)
    flare_gas_co2_pct: Optional[float] = Field(default=None, ge=0, le=100)
    flare_gas_n2_pct: Optional[float] = Field(default=None, ge=0, le=100)
    flare_combustion_efficiency: float = Field(default=0.98, ge=0, le=1)


# -------- BLOCK H — outbound logistics --------
class OutboundShipment(CarbonModel):
    facility_id: str
    shipment_date: date
    port_of_loading: str
    port_of_discharge: str
    vessel_name: Optional[str] = None
    cargo_tonnes: float = Field(ge=0)
    cn_code: str
    sea_distance_nm: Optional[float] = None
    bill_of_lading_path: Optional[str] = None
    eu_importer_name: Optional[str] = None
    customs_invoice_value_eur: Optional[float] = None


# -------- BLOCK K — monitoring meta --------
class MonitoringMeta(CarbonModel):
    facility_id: str
    period_start: date
    period_end: date
    monitoring_method: MonitoringMethod
    emission_factor_source: str
    gwp_set: GwpSet
    meter_id: Optional[str] = None
    last_calibration_date: Optional[date] = None
    verifier_name: Optional[str] = None
    verifier_accreditation_id: Optional[str] = None
    verification_opinion: VerificationOpinion = VerificationOpinion.NOT_VERIFIED
    verification_report_path: Optional[str] = None
    sampling_frequency: SamplingFrequency = SamplingFrequency.MONTHLY
    uncertainty_pct: float = Field(default=10.0, ge=0, le=100)  # ±%
    material_misstatements: list[dict[str, Any]] = Field(default_factory=list)
    notes: Optional[str] = None


# -------- documents (OCR'd raw + extracted fields) --------
class InvoiceDocument(CarbonModel):
    file_path: str
    vendor_name: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    category: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    raw_text: Optional[str] = None
    ocr_confidence: Optional[float] = Field(default=None, ge=0, le=1)
    needs_manual_review: bool = False


# -------- NEW MODELS: closes the remaining CBAM checklist gaps -----------

class ProcessBoundary(CarbonModel):
    """Section 4 — system boundary description per CBAM IR Annex IV §A.4."""
    facility_id: str
    product_cn_code: str
    aggregated_goods_category: str   # e.g. "primary aluminium", "urea"
    boundary_description: str        # free-text but mandatory
    included_unit_processes: list[str] = Field(default_factory=list)
    excluded_unit_processes: list[str] = Field(default_factory=list)
    process_diagram_path: Optional[str] = None
    effective_from: date
    effective_to: Optional[date] = None


class RECsCertificate(CarbonModel):
    """Section 6 — RECs / Guarantees of Origin as a first-class record."""
    facility_id: str
    period_start: date
    period_end: date
    certificate_type: str            # "REC", "GO", "I-REC"
    registry: str                    # "AIB", "M-RETS", etc.
    certificate_id: str
    mwh: float = Field(ge=0)
    generation_source: str           # solar / wind / hydro / nuclear / geothermal
    generation_country: str
    vintage_year: int
    retired: bool = True
    document_path: Optional[str] = None


class CHPRecord(CarbonModel):
    """Section 6 — Combined Heat & Power output (electrical + thermal)."""
    facility_id: str
    period_start: date
    period_end: date
    electrical_output_kwh: float = Field(default=0, ge=0)
    thermal_output_gj: float = Field(default=0, ge=0)
    fuel_input_gj: float = Field(default=0, ge=0)
    fuel_type: Optional[FuelType] = None
    overall_efficiency_pct: Optional[float] = Field(default=None, ge=0, le=100)


class CarbonPricePaid(CarbonModel):
    """Section 8 / Block G — carbon price paid in origin country (deductible)."""
    facility_id: str
    period_start: date
    period_end: date
    tax_type: str                            # e.g. "SA Carbon Tax Act 15/2019"
    tax_legislation_ref: Optional[str] = None
    gross_emissions_tco2e: float = Field(ge=0)
    tax_free_allowances_pct: float = Field(default=0, ge=0, le=100)
    net_taxable_tco2e: float = Field(ge=0)
    rate_local_per_tco2e: float = Field(ge=0)
    local_currency: str
    total_paid_local: float = Field(ge=0)
    total_paid_eur: float = Field(ge=0)
    fx_rate_local_to_eur: float = Field(gt=0)
    payment_receipt_path: Optional[str] = None
    free_allocation_tco2e: float = Field(default=0, ge=0)


class MRPlan(CarbonModel):
    """Section 9 — Monitoring & Reporting Plan (mandatory artefact)."""
    facility_id: str
    plan_version: str
    effective_from: date
    effective_to: Optional[date] = None
    approved_by: Optional[str] = None
    plan_document_path: Optional[str] = None
    summary: Optional[str] = None
    covered_emission_sources: list[str] = Field(default_factory=list)


class CostCentreAllocation(CarbonModel):
    """Allocates Block C2.2 electricity (and other utilities) to cost centres."""
    facility_id: str
    period_start: date
    period_end: date
    cost_centre: str
    cost_centre_id: Optional[str] = None
    parent_cost_centre: Optional[str] = None
    allocated_kwh: float = Field(default=0, ge=0)
    allocated_steam_gj: float = Field(default=0, ge=0)
    allocation_basis: AllocationMethod = AllocationMethod.MASS
    notes: Optional[str] = None


class StockMovement(CarbonModel):
    """Goods movement (ERPNext `Stock Entry` / SAP MSEG equivalent) — closes
    the three-way audit chain PO → GR → Invoice."""
    facility_id: str
    movement_date: date
    item_code: str
    item_cn_code: Optional[str] = None
    qty: float
    unit: UnitOfMeasure
    movement_type: str               # "receive" / "issue" / "transfer" / "consume"
    work_order_id: Optional[str] = None
    purchase_order_id: Optional[str] = None
    cost_centre: Optional[str] = None


class GLEntry(CarbonModel):
    """Financial GL line — for finance ↔ activity-data reconciliation."""
    facility_id: str
    posting_date: date
    voucher_type: str                # "Purchase Invoice" / "Journal Entry"
    voucher_no: str
    account: str
    debit_local: float = Field(default=0, ge=0)
    credit_local: float = Field(default=0, ge=0)
    currency: str
    cost_centre: Optional[str] = None
    against_item_code: Optional[str] = None


class QualityInspection(CarbonModel):
    """Quality checks on work orders — closes the reject/rework feedback loop."""
    facility_id: str
    inspection_date: date
    work_order_id: str
    item_code: str
    result: str                      # "pass" / "rework" / "reject"
    defect_code: Optional[str] = None
    inspector: Optional[str] = None
    rework_work_order_id: Optional[str] = None


# -------- audit trail --------
class IngestionEvent(BaseModel):
    """Stamped on every ingest call — gives operations a single audit log."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=_new_id)
    source: SourceMethod
    stream: str
    record_count: int = 0
    ok_count: int = 0
    error_count: int = 0
    started_at: datetime = Field(default_factory=_utcnow)
    finished_at: Optional[datetime] = None
    raw_path: Optional[str] = None
    notes: Optional[str] = None
