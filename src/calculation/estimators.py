"""Estimators that fill missing CBAM fields with IPCC / Annex defaults plus
the ±uncertainty band CBAM IR 2023/1773 Art.4(3) permits for transitional
reporting.

Every estimator returns a value *and* an `EstimatedValue` wrapper that
carries provenance, uncertainty %, and the EF tier — so the renderer can
flag products where >20% of emissions come from estimates.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import lookup_tables as lut


@dataclass(frozen=True)
class EstimatedValue:
    value: float
    uncertainty_pct: float
    tier: str                   # "measured" | "supplier_actual" | "national" | "ipcc_default" | "cbam_default" | "estimated"
    source: str                 # citation


# ---------------------------------------------------------------------------
# NCV / carbon content / oxidation factor — CBAM Section 5
# ---------------------------------------------------------------------------

def estimate_ncv(fuel_type: str, measured: Optional[float] = None) -> EstimatedValue:
    """Net calorific value (GJ per native fuel unit)."""
    if measured and measured > 0:
        return EstimatedValue(measured, 2.5, "measured", "lab cert (Tier 3)")
    d = lut.fuel_default(fuel_type)
    if not d:
        return EstimatedValue(40.0, 25.0, "estimated", "fallback assumption")
    return EstimatedValue(d.ncv_gj_per_unit, d.uncertainty_pct, "ipcc_default", d.source)


def estimate_carbon_content(fuel_type: str, measured: Optional[float] = None) -> EstimatedValue:
    if measured and measured > 0:
        return EstimatedValue(measured, 2.5, "measured", "lab cert")
    d = lut.fuel_default(fuel_type)
    if not d:
        return EstimatedValue(80.0, 25.0, "estimated", "fallback")
    return EstimatedValue(d.carbon_content_pct, d.uncertainty_pct, "ipcc_default", d.source)


def estimate_oxidation_factor(fuel_type: str, measured: Optional[float] = None) -> EstimatedValue:
    if measured and measured > 0:
        return EstimatedValue(measured, 1.0, "measured", "site test")
    d = lut.fuel_default(fuel_type)
    if not d:
        return EstimatedValue(0.99, 2.0, "estimated", "fallback")
    return EstimatedValue(d.oxidation_factor, 2.0, "ipcc_default", d.source)


def estimate_fuel_ef_kg_co2_per_gj(fuel_type: str, measured: Optional[float] = None) -> EstimatedValue:
    if measured and measured > 0:
        return EstimatedValue(measured, 3.0, "measured", "lab cert")
    d = lut.fuel_default(fuel_type)
    if not d:
        return EstimatedValue(74.0, 20.0, "estimated", "fallback")
    return EstimatedValue(d.ef_kg_co2_per_gj, d.uncertainty_pct, "ipcc_default", d.source)


# ---------------------------------------------------------------------------
# Embedded emissions for a precursor CN code — Section 7
# ---------------------------------------------------------------------------

def estimate_precursor_ee(
    cn_code: str,
    supplier_actual: Optional[float] = None,
) -> EstimatedValue:
    if supplier_actual and supplier_actual > 0:
        return EstimatedValue(supplier_actual, 8.0, "supplier_actual",
                              "supplier portal declaration (verified)")
    default = lut.cbam_default_embedded(cn_code)
    if default:
        return EstimatedValue(default["total"], default["uncertainty_pct"],
                              "cbam_default",
                              f"CBAM IR 2023/1773 Annex VIII (CN {cn_code})")
    return EstimatedValue(2.0, 25.0, "estimated",
                          f"fallback for unmapped CN {cn_code}; ±20% buffer")


# ---------------------------------------------------------------------------
# Grid + steam emission factors — Section 6
# ---------------------------------------------------------------------------

def estimate_grid_ef(country: str, supplier_specific: Optional[float] = None) -> EstimatedValue:
    if supplier_specific and supplier_specific > 0:
        return EstimatedValue(supplier_specific, 5.0, "supplier_actual",
                              "market-based supplier-specific EF")
    g = lut.GRID_EF_KG_CO2_PER_KWH.get(country)
    if g is not None:
        return EstimatedValue(g, 10.0, "national",
                              f"national grid EF for {country}")
    return EstimatedValue(0.5, 25.0, "estimated", "global fallback")


def estimate_steam_ef(supplier_specific: Optional[float] = None) -> EstimatedValue:
    if supplier_specific and supplier_specific > 0:
        return EstimatedValue(supplier_specific, 8.0, "supplier_actual", "supplier-specific")
    return EstimatedValue(lut.DEFAULT_STEAM_EF_KG_CO2_PER_GJ,
                          lut.DEFAULT_STEAM_EF_UNCERTAINTY_PCT,
                          "ipcc_default",
                          "gas-boiler approximation")


# ---------------------------------------------------------------------------
# Process emissions — anode + PFC + ammonia + nitric acid + urea
# ---------------------------------------------------------------------------

def estimate_anode_co2_t(anode_consumed_t: float) -> EstimatedValue:
    """Pre-bake anode CO2 emission per t anode consumed (≈ 3.45 kg CO2/kg)."""
    return EstimatedValue(
        anode_consumed_t * lut.ANODE_CO2_KG_PER_KG_NET,
        5.0, "ipcc_default", "IPCC V3 Ch4 Eq 4.20 (pre-bake)",
    )


def estimate_pfc_co2e_t(
    al_tonnes: float,
    route: str = "PRIMARY_PREBAKE",
    anode_effect_minutes_per_pot_day: Optional[float] = None,
    gwp_set: str = "AR6",
) -> EstimatedValue:
    """PFC emissions for aluminium smelters (CF4 + C2F6) — Tier-1 or slope-based."""
    if anode_effect_minutes_per_pot_day and anode_effect_minutes_per_pot_day > 0:
        slope = lut.PFC_SLOPE_KG_PER_AE_MIN[route]
        cf4_kg = slope["CF4"] * anode_effect_minutes_per_pot_day * al_tonnes
        c2f6_kg = slope["C2F6"] * anode_effect_minutes_per_pot_day * al_tonnes
        tier = "national"
        unc = 10.0
        src = "IPCC V3 Ch4 Tier-2 slope method"
    else:
        d = lut.PFC_DEFAULTS_KG_PER_T_AL[route]
        cf4_kg = d["CF4"] * al_tonnes
        c2f6_kg = d["C2F6"] * al_tonnes
        tier = "ipcc_default"
        unc = 15.0
        src = "IPCC V3 Ch4 Tier-1 default"
    co2e_t = (cf4_kg / 1000) * lut.gwp("CF4", gwp_set) + (c2f6_kg / 1000) * lut.gwp("C2F6", gwp_set)
    return EstimatedValue(co2e_t, unc, tier, src)


def estimate_nh3_smr_process_co2_t(ng_feedstock_nm3: float) -> EstimatedValue:
    """Process CO2 from SMR feedstock — kg CO2 per Nm3 NG → tonnes."""
    return EstimatedValue(
        ng_feedstock_nm3 * lut.NH3_SMR_CO2_KG_PER_NM3_NG / 1000.0,
        10.0, "ipcc_default", "IPCC V3 Ch3 SMR stoichiometry",
    )


def estimate_hno3_n2o_tco2e(
    nitric_acid_t: float,
    abatement: str = "secondary_catalyst",
    gwp_set: str = "AR6",
) -> EstimatedValue:
    n2o_kg = nitric_acid_t * lut.HNO3_N2O_KG_PER_T.get(abatement, 1.5)
    co2e_t = (n2o_kg / 1000.0) * lut.gwp("N2O", gwp_set)
    return EstimatedValue(co2e_t, 12.0, "ipcc_default", "IPCC V3 Ch3.3 default")


def estimate_urea_co2_used_t(urea_t: float) -> EstimatedValue:
    return EstimatedValue(urea_t * lut.UREA_CO2_USED_PER_T, 5.0,
                          "ipcc_default", "stoichiometric (urea synthesis)")


# ---------------------------------------------------------------------------
# Fugitive (refrigerants + SF6 + flaring)
# ---------------------------------------------------------------------------

def estimate_refrigerant_co2e_t(
    refrigerant: str, topup_kg: float, gwp_set: str = "AR6",
) -> EstimatedValue:
    g = lut.gwp(refrigerant, gwp_set)
    return EstimatedValue(topup_kg * g / 1000.0, 10.0, "ipcc_default",
                          f"{gwp_set} GWP for {refrigerant}")


def estimate_sf6_co2e_t(topup_kg: float, gwp_set: str = "AR6") -> EstimatedValue:
    return EstimatedValue(topup_kg * lut.gwp("SF6", gwp_set) / 1000.0,
                          8.0, "ipcc_default", f"{gwp_set} GWP for SF6")


def estimate_flaring_co2e_t(
    flaring_nm3: float,
    ch4_pct: Optional[float] = None,
    combustion_efficiency: float = 0.98,
    gwp_set: str = "AR6",
) -> EstimatedValue:
    """Treat flared gas as natural-gas-equivalent unless composition given."""
    ch4_frac = (ch4_pct or 90.0) / 100.0
    # combusted CH4 → CO2; uncombusted CH4 → CH4 vented
    combusted_ch4_kg = flaring_nm3 * ch4_frac * 0.717 * combustion_efficiency  # 0.717 kg/Nm3 (CH4)
    vented_ch4_kg = flaring_nm3 * ch4_frac * 0.717 * (1 - combustion_efficiency)
    co2_from_combustion_kg = combusted_ch4_kg * (44 / 16)  # CH4 + 2O2 -> CO2
    co2e_t = (co2_from_combustion_kg + vented_ch4_kg * lut.gwp("CH4", gwp_set)) / 1000.0
    return EstimatedValue(co2e_t, 18.0, "ipcc_default", "IPCC V2 Ch4 flaring")


# ---------------------------------------------------------------------------
# Sea distance fallback for outbound shipments
# ---------------------------------------------------------------------------

def estimate_sea_distance_nm(loading: str, discharge: str) -> EstimatedValue:
    d = lut.sea_distance(loading, discharge)
    if d:
        return EstimatedValue(d, 5.0, "national", "MarineTraffic-equivalent lookup")
    return EstimatedValue(5_000, 20.0, "estimated", "fallback global average")
