"""The CBAM formulas — pure functions, no I/O.

Direct SEE:
    sum( fuel_qty × NCV × EF × OF ) + sum( process_emissions )   [tCO2e]
    ─────────────────────────────────────────────────────────── = tCO2e / t
                              output_tonnes

Indirect SEE:
    electricity_kWh × grid_EF + steam_GJ × steam_EF              [tCO2e]
    ───────────────────────────────────────────────────────────── = tCO2e / t
                              output_tonnes

Complex-goods SEE:
    direct + indirect + Σ (precursor_qty × precursor_EE)

Adjusted SEE:
    SEE − ( carbon_price_paid_local / EUA_price ) × FX

References: CBAM IR 2023/1773 Annex IV §A.4 and Annex VIII Part C.
"""
from __future__ import annotations

from .estimators import EstimatedValue
from .result_models import EmissionLine
from .uncertainty import Uncertainty


# ---------------------------------------------------------------------------
# Direct emissions
# ---------------------------------------------------------------------------

def fuel_combustion_emissions_t(
    activity_value: float,
    activity_unit: str,
    ncv: EstimatedValue,
    ef_kg_per_gj: EstimatedValue,
    oxidation: EstimatedValue,
    label: str,
) -> EmissionLine:
    """Activity × NCV × EF × OF → tCO2.

    For gases the convention is `activity` in Nm3 and `ncv` expressed per
    1000 Nm3 — convert in the caller. Here we treat `ncv.value` as GJ per
    (activity_unit), so the dimensional analysis is uniform.
    """
    co2_kg = activity_value * ncv.value * ef_kg_per_gj.value * oxidation.value
    co2_t = co2_kg / 1000.0
    # combine relative uncertainties (RSS — NCV, EF, OF are independent)
    from .uncertainty import combine_relative
    rel_unc = combine_relative(ncv.uncertainty_pct, ef_kg_per_gj.uncertainty_pct,
                               oxidation.uncertainty_pct)
    tier = _weakest_tier(ncv.tier, ef_kg_per_gj.tier, oxidation.tier)
    return EmissionLine(
        category="fuel",
        label=label,
        activity_value=activity_value, activity_unit=activity_unit,
        ef_value=ef_kg_per_gj.value, ef_unit="kg CO2/GJ",
        ef_tier=tier, ef_source=ef_kg_per_gj.source,
        co2e_tonnes=co2_t,
        uncertainty_pct=rel_unc,
        is_estimated=tier in ("ipcc_default", "cbam_default", "estimated"),
    )


def process_emission_line(
    label: str,
    co2e_estimate: EstimatedValue,
    activity_value: float,
    activity_unit: str,
) -> EmissionLine:
    """Wrap an EstimatedValue (already in tCO2e) as a process emission line."""
    return EmissionLine(
        category="process",
        label=label,
        activity_value=activity_value, activity_unit=activity_unit,
        ef_value=1.0, ef_unit="tCO2e/unit",
        ef_tier=co2e_estimate.tier, ef_source=co2e_estimate.source,
        co2e_tonnes=co2e_estimate.value,
        uncertainty_pct=co2e_estimate.uncertainty_pct,
        is_estimated=co2e_estimate.tier in ("ipcc_default", "cbam_default", "estimated"),
    )


# ---------------------------------------------------------------------------
# Indirect emissions
# ---------------------------------------------------------------------------

def electricity_emissions_t(
    kwh: float, grid_ef: EstimatedValue, label: str = "Grid electricity",
) -> EmissionLine:
    co2_t = kwh * grid_ef.value / 1000.0   # grid_ef is kg CO2/kWh
    return EmissionLine(
        category="electricity",
        label=label,
        activity_value=kwh, activity_unit="kWh",
        ef_value=grid_ef.value, ef_unit="kg CO2/kWh",
        ef_tier=grid_ef.tier, ef_source=grid_ef.source,
        co2e_tonnes=co2_t, uncertainty_pct=grid_ef.uncertainty_pct,
        is_estimated=grid_ef.tier in ("ipcc_default", "cbam_default", "estimated"),
    )


def steam_emissions_t(
    gj: float, steam_ef: EstimatedValue, label: str = "Purchased steam",
) -> EmissionLine:
    co2_t = gj * steam_ef.value / 1000.0   # steam_ef in kg CO2/GJ
    return EmissionLine(
        category="steam",
        label=label,
        activity_value=gj, activity_unit="GJ",
        ef_value=steam_ef.value, ef_unit="kg CO2/GJ",
        ef_tier=steam_ef.tier, ef_source=steam_ef.source,
        co2e_tonnes=co2_t, uncertainty_pct=steam_ef.uncertainty_pct,
        is_estimated=steam_ef.tier in ("ipcc_default", "cbam_default", "estimated"),
    )


# ---------------------------------------------------------------------------
# Precursor / complex-goods
# ---------------------------------------------------------------------------

def precursor_line(
    cn_code: str,
    quantity_tonnes: float,
    ee: EstimatedValue,
) -> EmissionLine:
    co2_t = quantity_tonnes * ee.value
    return EmissionLine(
        category="precursor",
        label=f"Precursor CN {cn_code}",
        activity_value=quantity_tonnes, activity_unit="tonnes",
        ef_value=ee.value, ef_unit="tCO2e/t",
        ef_tier=ee.tier, ef_source=ee.source,
        co2e_tonnes=co2_t, uncertainty_pct=ee.uncertainty_pct,
        is_estimated=ee.tier in ("cbam_default", "ipcc_default", "estimated"),
    )


# ---------------------------------------------------------------------------
# SEE math
# ---------------------------------------------------------------------------

def specific_embedded_emissions(
    direct_t: float, indirect_t: float, precursor_t: float, output_t: float,
) -> tuple[float, float, float]:
    """Returns (direct_see, indirect_see, total_see) in tCO2e per tonne output."""
    if output_t <= 0:
        return (0.0, 0.0, 0.0)
    direct_see = direct_t / output_t
    indirect_see = indirect_t / output_t
    total_see = (direct_t + indirect_t + precursor_t) / output_t
    return (direct_see, indirect_see, total_see)


def adjusted_see(
    see: float,
    carbon_price_eur_per_tco2e: float,
    eua_price_eur_per_tco2e: float,
) -> float:
    """CBAM IR Annex VIII Part D: deduct the carbon price actually paid in the
    country of origin from the certificate cost. Effectively `see × (EUA − cp) / EUA`."""
    if eua_price_eur_per_tco2e <= 0:
        return see
    adj = see * (1 - (carbon_price_eur_per_tco2e / eua_price_eur_per_tco2e))
    return max(0.0, adj)


def cbam_certificate_cost_eur(
    adjusted_see_t: float,
    eu_export_tonnes: float,
    eua_price: float,
) -> float:
    return adjusted_see_t * eu_export_tonnes * eua_price


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _weakest_tier(*tiers: str) -> str:
    order = ["measured", "supplier_actual", "national", "cbam_default", "ipcc_default", "estimated"]
    ranked = [t for t in tiers if t]
    if not ranked:
        return "estimated"
    return max(ranked, key=lambda t: order.index(t) if t in order else len(order))
