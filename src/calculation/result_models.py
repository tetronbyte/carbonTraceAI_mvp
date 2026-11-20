"""Pydantic models for the calculation engine outputs.

These are the shapes the dashboard, reports, and EU CBAM XML renderer
consume. They are deliberately *flat* — every field has a name, a value,
and a provenance entry so the verifier can trace every number back to a
raw source row.
"""
from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EmissionLine(BaseModel):
    """One contributing line to a product's direct or indirect emissions."""
    model_config = ConfigDict(extra="forbid")

    category: str                        # "fuel", "process", "electricity", "steam", "precursor", "fugitive"
    label: str                           # human-readable
    activity_value: float                # e.g. tonnes of fuel, kWh
    activity_unit: str
    ef_value: float                      # the EF used
    ef_unit: str
    ef_tier: str                         # measured / supplier_actual / national / ipcc_default / cbam_default / estimated
    ef_source: str
    co2e_tonnes: float
    uncertainty_pct: float
    is_estimated: bool


class ProductEmissions(BaseModel):
    """SEE breakdown for a single CN code in a single period."""
    model_config = ConfigDict(extra="forbid")

    facility_id: str
    product_cn_code: str
    product_name: str
    period_start: date
    period_end: date

    # core numbers
    output_tonnes: float
    eu_export_tonnes: float
    domestic_sales_tonnes: float

    # direct (Scope 1)
    direct_emissions_tco2e: float
    direct_lines: list[EmissionLine] = Field(default_factory=list)

    # indirect (Scope 2)
    indirect_emissions_tco2e: float
    indirect_lines: list[EmissionLine] = Field(default_factory=list)

    # precursors (Scope 3 / complex goods)
    precursor_emissions_tco2e: float
    precursor_lines: list[EmissionLine] = Field(default_factory=list)

    # specific embedded emissions (the headline CBAM number)
    direct_see_tco2_per_t: float
    indirect_see_tco2_per_t: float
    total_see_tco2_per_t: float
    adjusted_see_tco2_per_t: float       # after carbon-price-paid deduction

    # uncertainty
    overall_uncertainty_pct: float
    share_of_estimated_emissions: float  # 0–1; verifier flags > 0.20

    # carbon-price deduction
    carbon_price_paid_eur_per_tco2e: float = 0.0
    eua_price_eur_per_tco2e: float = 75.0

    # allocation
    coproduct_allocation_method: str = "none"
    allocation_share: float = 1.0

    # CBAM cost projection
    cbam_certificate_cost_eur: float = 0.0

    # default-value method (official table incl. mark-up); None = not a CBAM good
    default_see_tco2_per_t: Optional[float] = None
    default_cbam_certificate_cost_eur: Optional[float] = None
    default_value_source: Optional[str] = None


class FacilityReport(BaseModel):
    """All products for one facility in one reporting period."""
    model_config = ConfigDict(extra="forbid")

    facility_id: str
    legal_entity_name: str
    country: str
    sector: str
    cbam_installation_id: Optional[str] = None
    un_locode: Optional[str] = None
    eori: Optional[str] = None

    reporting_period_start: date
    reporting_period_end: date
    quarter: str                          # e.g. "2026-Q2"

    products: list[ProductEmissions] = Field(default_factory=list)

    # roll-up
    total_direct_tco2e: float = 0.0
    total_indirect_tco2e: float = 0.0
    total_precursor_tco2e: float = 0.0
    total_emissions_tco2e: float = 0.0
    eu_export_share: float = 0.0
    projected_cbam_cost_eur: float = 0.0

    # reconciliation
    mass_balance_residual_pct: Optional[float] = None
    energy_balance_residual_pct: Optional[float] = None
    finance_cross_check_residual_pct: Optional[float] = None

    # data-quality flags
    products_over_estimation_threshold: list[str] = Field(default_factory=list)
    missing_data_warnings: list[str] = Field(default_factory=list)


class CalculationRun(BaseModel):
    """Top-level container for a single calc run."""
    model_config = ConfigDict(extra="forbid")

    run_id: str
    started_at: str
    finished_at: Optional[str] = None
    facility_reports: list[FacilityReport] = Field(default_factory=list)
    notes: Optional[str] = None
