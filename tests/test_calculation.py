"""Tests for the CBAM calculation engine.

Strategy: seed the canonical Repository with realistic Pydantic payloads
(no ERPNext required), run the engine, assert on the produced
CalculationRun + XML/CSV renderer output.
"""
from datetime import date

import pytest

from src.calculation import CBAMCalculationEngine, EngineConfig, cbam_xml, cbam_csv, dashboard_json
from src.calculation import estimators as est
from src.calculation import formulas as F
from src.calculation import lookup_tables as lut
from src.calculation.allocation import allocate
from src.calculation.ef_priority import resolve
from src.calculation.uncertainty import combine_relative, combine_additive, Uncertainty
from src.core.enums import (
    AllocationMethod, AluminiumRoute, AnodeType, Country, FuelType,
    GwpSet, MeterType, MonitoringMethod, Sector, SourceMethod, UnitOfMeasure,
    VerificationOpinion, WorkOrderOutcome,
)
from src.core.models import (
    AluminiumProcessRecord, CarbonPricePaid, EnergyConsumption, Facility,
    FertiliserProcessRecord, FugitiveEmission, MonitoringMeta,
    PrecursorPurchase, ProductionRun, RECsCertificate,
)


# ---------------------------------------------------------------------------
# Lookup + estimator unit tests
# ---------------------------------------------------------------------------

def test_ipcc_natural_gas_default():
    d = lut.fuel_default("natural_gas")
    assert d is not None
    assert d.ef_kg_co2_per_gj == pytest.approx(56.1, rel=0.01)
    assert d.ncv_gj_per_unit == pytest.approx(39.0, rel=0.01)


def test_cbam_default_primary_aluminium():
    v = lut.cbam_default_embedded("76011000")
    assert v is not None
    assert v["total"] == pytest.approx(8.6, rel=0.01)


def test_gwp_ar6_cf4_higher_than_ar5():
    assert lut.gwp("CF4", "AR6") > lut.gwp("CF4", "AR5")


def test_grid_ef_mozambique_is_low_carbon():
    assert lut.GRID_EF_KG_CO2_PER_KWH["MZ"] < 0.10  # hydro-dominated


def test_estimator_falls_back_to_ipcc_when_no_measured():
    v = est.estimate_ncv("natural_gas")
    assert v.tier == "ipcc_default"
    assert v.uncertainty_pct > 0


def test_estimator_prefers_measured_when_available():
    v = est.estimate_ncv("natural_gas", measured=41.5)
    assert v.tier == "measured"
    assert v.value == 41.5
    assert v.uncertainty_pct < 5


def test_ef_priority_picks_measured_over_default():
    measured = est.EstimatedValue(0.85, 5.0, "measured", "lab")
    default = est.EstimatedValue(0.90, 10.0, "ipcc_default", "ipcc")
    picked = resolve(default, measured)
    assert picked.tier == "measured"


# ---------------------------------------------------------------------------
# Formula unit tests
# ---------------------------------------------------------------------------

def test_fuel_combustion_emissions_aluminium_casthouse():
    line = F.fuel_combustion_emissions_t(
        activity_value=10, activity_unit="1000 Nm3",
        ncv=est.estimate_ncv("natural_gas"),
        ef_kg_per_gj=est.estimate_fuel_ef_kg_co2_per_gj("natural_gas"),
        oxidation=est.estimate_oxidation_factor("natural_gas"),
        label="natural_gas — casthouse",
    )
    # 10 × 39 GJ × 56.1 kg/GJ × 1.0 OF ≈ 21,879 kg = 21.88 t CO2
    assert line.co2e_tonnes == pytest.approx(21.879, rel=0.02)
    assert line.is_estimated is True


def test_specific_embedded_emissions_split():
    direct, indirect, total = F.specific_embedded_emissions(100, 50, 30, 100)
    assert direct == 1.0
    assert indirect == 0.5
    assert total == pytest.approx(1.8)


def test_adjusted_see_deducts_carbon_price():
    adj = F.adjusted_see(see=10.0, carbon_price_eur_per_tco2e=15.0, eua_price_eur_per_tco2e=75.0)
    # 10 × (1 - 15/75) = 10 × 0.8 = 8.0
    assert adj == pytest.approx(8.0)


def test_adjusted_see_floored_at_zero():
    adj = F.adjusted_see(see=5, carbon_price_eur_per_tco2e=100, eua_price_eur_per_tco2e=75)
    assert adj == 0.0


def test_uncertainty_combines_in_quadrature():
    rel = combine_relative(10, 10)
    assert rel == pytest.approx(14.142, rel=0.01)


def test_allocation_mass_basis():
    out = allocate(100.0, {"A": 60, "B": 40}, AllocationMethod.MASS)
    assert out == {"A": 60.0, "B": 40.0}


# ---------------------------------------------------------------------------
# Engine integration — seed the repository, run the engine
# ---------------------------------------------------------------------------

def _seed_aluminium_facility(repo, q_start=date(2026, 4, 1), q_end=date(2026, 6, 30)):
    repo.save_many([Facility(
        source=SourceMethod.MANUAL,
        legal_entity_name="Mozal SA",
        company_registration_number="MZ-100", plant_operating_name="Mozal Smelter",
        physical_address="Beluluane", country=Country.MZ, sector=Sector.ALUMINIUM,
        cn_codes=["76011000"], reporting_period_start=q_start, reporting_period_end=q_end,
        design_capacity_t_per_year=580_000, functional_currency="USD",
        eori="MZ100123456789", un_locode="MZMPM", cbam_installation_id="MZ-INST-001",
    )])

    # Production: 50,000 t of primary Al, 60% to EU
    repo.save_many([ProductionRun(
        source=SourceMethod.ERP,
        facility_id="MOZAL-MZ-01",
        sector=Sector.ALUMINIUM,
        product_name="primary_aluminium_ingot",
        product_cn_code="76011000",
        batch_run_id="WO-Q2-001",
        output_tonnes=50_000,
        eu_export_tonnes=30_000, domestic_sales_tonnes=20_000,
        aluminium_route=AluminiumRoute.PRIMARY,
        anode_type=AnodeType.PRE_BAKE,
        run_started_at=q_start,
        run_ended_at=q_end,
    )])

    # Aluminium process: anode + PFC
    repo.save_many([AluminiumProcessRecord(
        source=SourceMethod.MANUAL,
        facility_id="MOZAL-MZ-01", period_start=q_start, period_end=q_end,
        anode_consumption_tonnes=21_500,
        primary_al_output_tonnes=50_000,
        anode_effect_minutes=0.12,
    )])

    # Electricity — low-carbon Mozambican grid
    repo.save_many([EnergyConsumption(
        source=SourceMethod.METER,
        facility_id="MOZAL-MZ-01", period_start=q_start, period_end=q_end,
        meter_type=MeterType.ELECTRICITY_GRID,
        quantity=750_000_000, unit=UnitOfMeasure.KWH, cost_centre="potline_1",
    )])

    # Precursor: alumina (CN 28182000), supplier-actual EE
    repo.save_many([PrecursorPurchase(
        source=SourceMethod.SUPPLIER,
        facility_id="MOZAL-MZ-01",
        po_number="PO-Q2-101",
        precursor_name="alumina",
        precursor_cn_code="28182000",
        quantity_tonnes=96_000,
        supplier_name="Alunorte", supplier_country="BR",
        embedded_emissions_tco2_per_t=1.05,
        ee_method="actual",
        purchase_date=q_start,
    )])

    repo.save_many([MonitoringMeta(
        source=SourceMethod.MANUAL,
        facility_id="MOZAL-MZ-01", period_start=q_start, period_end=q_end,
        monitoring_method=MonitoringMethod.TIER2,
        emission_factor_source="IPCC 2006 + supplier-actual",
        gwp_set=GwpSet.AR6,
        verifier_name="DNV", verifier_accreditation_id="DNV-CBAM-001",
        verification_opinion=VerificationOpinion.REASONABLE,
        uncertainty_pct=7.5,
    )])


def test_engine_runs_aluminium_facility(repo):
    _seed_aluminium_facility(repo)
    engine = CBAMCalculationEngine(repo)
    run = engine.run(quarter="2026-Q2")

    assert len(run.facility_reports) == 1
    fr = run.facility_reports[0]
    assert fr.country == "MZ"
    assert fr.cbam_installation_id == "MZ-INST-001"
    assert len(fr.products) == 1
    p = fr.products[0]
    assert p.product_cn_code == "76011000"
    assert p.output_tonnes == 50_000
    assert p.eu_export_tonnes == 30_000
    # Direct emissions = anode CO2 + PFC
    assert p.direct_emissions_tco2e > 50_000  # anode ≈ 74k t CO2 alone
    # Indirect: 750 GWh × 0.04 kg/kWh (Mozambique) = 30,000 t CO2
    assert p.indirect_emissions_tco2e == pytest.approx(30_000, rel=0.10)
    # Precursor: 96k t alumina × 1.05 tCO2e/t = 100,800 t
    assert p.precursor_emissions_tco2e == pytest.approx(100_800, rel=0.05)
    # SEE
    assert p.total_see_tco2_per_t > 2.0
    # CBAM cost: SEE × 30k t × €75
    assert p.cbam_certificate_cost_eur > 0


def test_carbon_price_deduction_reduces_adjusted_see(repo):
    _seed_aluminium_facility(repo)
    repo.save_many([CarbonPricePaid(
        source=SourceMethod.MANUAL,
        facility_id="MOZAL-MZ-01",
        period_start=date(2026, 4, 1), period_end=date(2026, 6, 30),
        tax_type="Generic carbon tax",
        gross_emissions_tco2e=10_000,
        net_taxable_tco2e=10_000,
        rate_local_per_tco2e=20.0,
        local_currency="EUR",
        total_paid_local=200_000,
        total_paid_eur=200_000,
        fx_rate_local_to_eur=1.0,
    )])

    run = CBAMCalculationEngine(repo).run(quarter="2026-Q2")
    p = run.facility_reports[0].products[0]
    assert p.carbon_price_paid_eur_per_tco2e == pytest.approx(20.0, rel=0.01)
    assert p.adjusted_see_tco2_per_t < p.total_see_tco2_per_t


def test_recs_reduce_indirect_emissions(repo):
    _seed_aluminium_facility(repo)
    repo.save_many([RECsCertificate(
        source=SourceMethod.MANUAL,
        facility_id="MOZAL-MZ-01",
        period_start=date(2026, 4, 1), period_end=date(2026, 6, 30),
        certificate_type="I-REC", registry="I-REC Standard",
        certificate_id="IREC-2026-MZ-001",
        mwh=500_000, generation_source="solar",
        generation_country="MZ", vintage_year=2026,
    )])
    run = CBAMCalculationEngine(repo).run(quarter="2026-Q2")
    p = run.facility_reports[0].products[0]
    # 500 GWh of RECs against 750 GWh consumed → indirect drops to ~1/3 of original
    assert p.indirect_emissions_tco2e < 15_000


def test_xml_renderer_includes_required_cbam_sections(repo):
    _seed_aluminium_facility(repo)
    run = CBAMCalculationEngine(repo).run(quarter="2026-Q2")
    xml = cbam_xml(run)
    for tag in (
        "QuarterlyReport", "Installation", "FacilityId", "CbamInstallationId",
        "EORI", "UNLOCODE", "Country", "Quarter", "Goods", "Good", "ProductName",
        "OutputTonnes", "EUExportTonnes", "EmbeddedEmissions", "DirectSEE",
        "IndirectSEE", "TotalSEE", "AdjustedSEE", "OverallUncertaintyPct",
        "EmissionLines", "Line", "EFSource",
    ):
        assert tag in xml, f"missing {tag} in CBAM XML"


def test_csv_renderer_one_row_per_product(repo):
    _seed_aluminium_facility(repo)
    run = CBAMCalculationEngine(repo).run(quarter="2026-Q2")
    csv = cbam_csv(run)
    lines = csv.strip().splitlines()
    assert lines[0].startswith("run_id,quarter,facility_id")
    assert len(lines) == 2   # header + 1 product
    assert "76011000" in lines[1]


def test_dashboard_json_has_totals_and_lines(repo):
    _seed_aluminium_facility(repo)
    run = CBAMCalculationEngine(repo).run(quarter="2026-Q2")
    import json
    d = json.loads(dashboard_json(run))
    assert "facilities" in d
    fac = d["facilities"][0]
    assert "totals" in fac
    assert fac["totals"]["totalTCO2e"] > 0
    assert fac["products"][0]["lines"]
