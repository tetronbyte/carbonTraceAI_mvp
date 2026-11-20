"""CBAM lookup tables — IPCC + CBAM Annex defaults the calc engine falls back to
when measured / supplier-actual data is unavailable.

Sources (citation-ready for the verifier):
  - IPCC 2006 Guidelines for National GHG Inventories, Vol 2 Ch 1 Table 1.2
    (default NCV) and Table 1.4 (default carbon EFs).
  - IPCC 2006 Guidelines, Vol 3 Ch 4 (PFC defaults for aluminium).
  - IPCC AR5 / AR6 100-year GWPs (Table 7.SM.7).
  - CBAM default values: IR 2025/2621 Annex I as replaced by IR 2026/1740
    (data/cbam_default_values_2026_1740.csv).

Every default has a *value*, a *unit*, and a *±uncertainty %*. The calc engine
propagates the uncertainty into the final SEE — defaults carry larger bands
than measured data, which lets the audit report flag products that exceed
the 20% estimated-emissions threshold (CBAM IR Art.4(3)).
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class FuelDefault:
    """IPCC Tier-1 defaults per fuel — combustion only."""
    fuel_code: str
    ncv_gj_per_unit: float
    ncv_unit: str                # "tonne" or "1000Nm3"
    carbon_content_pct: float    # % by mass (or by volume for gases)
    ef_kg_co2_per_gj: float      # IPCC Tier-1
    oxidation_factor: float
    uncertainty_pct: float       # ± band on the EF
    source: str = "IPCC 2006 V2 Ch1 Table 1.2 / 1.4"


# ---------------------------------------------------------------------------
# Fuel defaults
# ---------------------------------------------------------------------------
FUEL_DEFAULTS: dict[str, FuelDefault] = {
    "natural_gas": FuelDefault(
        fuel_code="natural_gas",
        ncv_gj_per_unit=39.0, ncv_unit="1000Nm3",
        carbon_content_pct=75.0, ef_kg_co2_per_gj=56.1,
        oxidation_factor=1.00, uncertainty_pct=10.0,
    ),
    "diesel": FuelDefault(
        fuel_code="diesel",
        ncv_gj_per_unit=43.0, ncv_unit="tonne",
        carbon_content_pct=86.0, ef_kg_co2_per_gj=74.1,
        oxidation_factor=0.99, uncertainty_pct=8.0,
    ),
    "heavy_fuel_oil": FuelDefault(
        fuel_code="heavy_fuel_oil",
        ncv_gj_per_unit=40.4, ncv_unit="tonne",
        carbon_content_pct=85.0, ef_kg_co2_per_gj=77.4,
        oxidation_factor=0.99, uncertainty_pct=8.0,
    ),
    "lpg": FuelDefault(
        fuel_code="lpg",
        ncv_gj_per_unit=47.3, ncv_unit="tonne",
        carbon_content_pct=82.0, ef_kg_co2_per_gj=63.1,
        oxidation_factor=1.00, uncertainty_pct=10.0,
    ),
    "coal": FuelDefault(
        fuel_code="coal",
        ncv_gj_per_unit=25.8, ncv_unit="tonne",
        carbon_content_pct=72.0, ef_kg_co2_per_gj=94.6,
        oxidation_factor=0.98, uncertainty_pct=12.0,
    ),
    "coke": FuelDefault(
        fuel_code="coke",
        ncv_gj_per_unit=28.2, ncv_unit="tonne",
        carbon_content_pct=87.0, ef_kg_co2_per_gj=107.0,
        oxidation_factor=0.98, uncertainty_pct=12.0,
    ),
    "biomass": FuelDefault(
        fuel_code="biomass",
        ncv_gj_per_unit=15.6, ncv_unit="tonne",
        carbon_content_pct=50.0, ef_kg_co2_per_gj=0.0,   # biogenic — excluded
        oxidation_factor=0.98, uncertainty_pct=15.0,
    ),
}


def fuel_default(fuel: str) -> Optional[FuelDefault]:
    return FUEL_DEFAULTS.get(fuel)


def kg_co2_per_unit(fuel: str) -> float:
    """Total kg CO2 per native fuel unit (tonne or 1000 Nm3) using IPCC Tier-1.

    Formula: kg CO2/unit = NCV × EF × OF (carbon_content is implicit in the EF).
    """
    f = FUEL_DEFAULTS.get(fuel)
    if not f:
        return 0.0
    return f.ncv_gj_per_unit * f.ef_kg_co2_per_gj * f.oxidation_factor


# ---------------------------------------------------------------------------
# Official CBAM default values (tCO2e/t): IR 2025/2621 Annex I as replaced by
# IR 2026/1740. CSV built by scripts/build_cbam_defaults.py from the OJ HTML.
# ---------------------------------------------------------------------------
CBAM_DEFAULTS_REG = "IR 2025/2621 Annex I as replaced by IR 2026/1740"
CBAM_DEFAULTS_CSV = Path(__file__).resolve().parents[2] / "data" / "cbam_default_values_2026_1740.csv"
_OTHER = "other countries and territories"

# ISO2 -> country table name in the OJ annex.
# shortcut: only countries the MVP or its target market uses; add a row per new country (unmapped -> Other table).
_EU_COUNTRY_NAME = {
    "MZ": "Mozambique", "MA": "Morocco", "ZA": "South Africa", "EG": "Egypt",
    "TZ": "Tanzania, United Republic of", "KE": "Kenya", "UG": "Uganda", "RW": "Rwanda",
    "ET": "Ethiopia", "ZM": "Zambia", "ZW": "Zimbabwe", "NG": "Nigeria", "GH": "Ghana",
    "DZ": "Algeria", "TN": "Tunisia", "BR": "Brazil", "CD": "Congo, Democratic Republic of",
}

# Not in the regulation: uncertainty band the MVP attaches to any default value.
CBAM_DEFAULT_UNCERTAINTY_PCT = 20.0


@lru_cache(maxsize=1)
def _official_defaults() -> dict[str, dict[str, tuple[Optional[float], str]]]:
    """{country lower: {cn_code: (total or None for "-", sector)}}."""
    out: dict[str, dict[str, tuple[Optional[float], str]]] = {}
    with CBAM_DEFAULTS_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["country"].lower(), {})[r["cn_code"]] = (
                float(r["total"]) if r["total"] else None, r["sector"])
    return out


def _longest_prefix(table: dict, cn: str):
    hits = [c for c in table if cn.startswith(c)]
    return table[max(hits, key=len)] if hits else None


def cbam_markup_pct(sector: str, year: int) -> float:
    """Annex I intro: 1 % for fertilisers; 10/20/30 % (2026/2027/2028+) otherwise."""
    if sector == "Fertilisers":
        return 1.0
    return 10.0 if year <= 2026 else 20.0 if year == 2027 else 30.0


def cbam_default(cn_code: str, iso2: Optional[str], year: int) -> Optional[dict]:
    """Official default (TOTAL column, recital 10) for a good, with mark-up.

    Longest CN/TARIC prefix match in the country table; country unmapped or
    value "-" -> "Other Countries and Territories". None = not a CBAM good.
    shortcut: a CN shorter than the table's TARIC codes (e.g. 8-digit clinker vs 10-digit) finds no match there.
    """
    cn = "".join(ch for ch in cn_code if ch.isdigit())
    tables = _official_defaults()
    name = _EU_COUNTRY_NAME.get((iso2 or "").upper(), _OTHER).lower()
    hit = _longest_prefix(tables.get(name, {}), cn)
    if not hit or hit[0] is None:
        name, hit = _OTHER, _longest_prefix(tables[_OTHER], cn)
    if not hit or hit[0] is None:
        return None
    base, sector = hit
    markup = cbam_markup_pct(sector, year)
    return {"base": base, "total": base * (1 + markup / 100), "markup_pct": markup,
            "sector": sector, "table": name, "uncertainty_pct": CBAM_DEFAULT_UNCERTAINTY_PCT}


# ---------------------------------------------------------------------------
# Process-emission defaults
# ---------------------------------------------------------------------------

# Pre-bake anode CO2: kg CO2 per kg net anode consumed (IPCC V3 Ch4 Eq 4.20)
# Assuming 85% C, S 2%, ash 0.4%, with full oxidation
ANODE_CO2_KG_PER_KG_NET = 3.45    # ≈ 0.43 t anode/t Al × 3.45 ≈ 1.48 t CO2/t Al

# PFC defaults — kg PFC per tonne Al (IPCC Tier 1, Modern PFPB / Søderberg)
PFC_DEFAULTS_KG_PER_T_AL = {
    "PRIMARY_PREBAKE": {"CF4": 0.04,  "C2F6": 0.004},
    "PRIMARY_SODERBERG":{"CF4": 0.07, "C2F6": 0.0056},
}

# Slope and overvoltage methods (CBAM Annex III sect. 8.A.3) — slope coefficients
PFC_SLOPE_KG_PER_AE_MIN = {
    "PRIMARY_PREBAKE":  {"CF4": 0.143, "C2F6": 0.0121},
    "PRIMARY_SODERBERG":{"CF4": 0.272, "C2F6": 0.0091},
}

# Ammonia SMR: kg CO2 per Nm3 natural-gas feedstock (process emissions only)
NH3_SMR_CO2_KG_PER_NM3_NG = 1.96   # ≈ 1.6 tCO2/tNH3 at 850 Nm3/tNH3

# Nitric acid N2O — IPCC Tier-1 default emission factor with destruction
HNO3_N2O_KG_PER_T = {
    "no_abatement":    7.5,
    "secondary_catalyst": 1.5,
    "tertiary_catalyst":  0.4,
}

# Urea synthesis: CO2 used = 0.78 t CO2 / t urea (matches BOM)
UREA_CO2_USED_PER_T = 0.78


# ---------------------------------------------------------------------------
# GWPs (100-year)
# ---------------------------------------------------------------------------
GWP_AR5 = {
    "CO2": 1, "CH4": 28, "N2O": 265, "CF4": 6_630, "C2F6": 11_100,
    "SF6": 23_500, "HFC-134a": 1_300, "HFC-23": 12_400,
    "HFC-32": 677, "R-410A": 1_924, "R-22": 1_760,
}

GWP_AR6 = {
    "CO2": 1, "CH4": 27.9, "N2O": 273, "CF4": 7_380, "C2F6": 12_400,
    "SF6": 24_300, "HFC-134a": 1_530, "HFC-23": 14_600,
    "HFC-32": 771, "R-410A": 2_256, "R-22": 1_960,
}


def gwp(gas: str, gwp_set: str = "AR6") -> float:
    table = GWP_AR6 if gwp_set.upper() == "AR6" else GWP_AR5
    return table.get(gas, 0)


# ---------------------------------------------------------------------------
# Country grid emission factors (kg CO2 / kWh) — keep in lockstep with
# config/data_dictionary.yaml. Indirect emissions use these.
# ---------------------------------------------------------------------------
GRID_EF_KG_CO2_PER_KWH = {
    "ZA": 0.90,
    "MZ": 0.04,
    "MA": 0.62,
    "EG": 0.45,
}

# Heat / steam emission factor when supplier-specific is unavailable.
DEFAULT_STEAM_EF_KG_CO2_PER_GJ = 70.0  # gas-fired boiler approximation
DEFAULT_STEAM_EF_UNCERTAINTY_PCT = 20.0


# ---------------------------------------------------------------------------
# Sea distance lookup (port pairs) — keep small; production replaces with
# a maritime distance API or the MarineTraffic database.
# ---------------------------------------------------------------------------
SEA_DISTANCE_NM = {
    ("MZMPM", "NLRTM"): 7_650,   # Maputo → Rotterdam
    ("MZMPM", "DEHAM"): 7_800,   # Maputo → Hamburg
    ("MAJEN", "FRMAR"): 1_240,   # Jorf Lasfar → Marseille
    ("MAJEN", "ESBAR"): 950,     # Jorf Lasfar → Barcelona
    ("MAJEN", "NLRTM"): 1_780,   # Jorf Lasfar → Rotterdam
    ("ZADUR", "DEHAM"): 7_550,   # Durban → Hamburg
    ("EGALY", "ITGOA"): 1_280,   # Alexandria → Genoa
}


def sea_distance(loading: str, discharge: str) -> Optional[float]:
    return SEA_DISTANCE_NM.get((loading.upper(), discharge.upper()))


# ---------------------------------------------------------------------------
# Foreign-exchange floor table (when no live FX feed is available).
# Local currency → EUR rate; replace from ECB feed in production.
# ---------------------------------------------------------------------------
FX_TO_EUR = {
    "EUR": 1.00,
    "USD": 0.92,
    "ZAR": 0.050,
    "MZN": 0.014,
    "MAD": 0.092,
    "EGP": 0.019,
}


def fx_to_eur(currency: str) -> float:
    return FX_TO_EUR.get(currency.upper(), 1.0)


# EUA carbon price reference (replace with live spot in production).
EUA_PRICE_EUR_PER_TCO2E = 75.0
