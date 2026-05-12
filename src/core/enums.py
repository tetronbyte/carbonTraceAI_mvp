"""Controlled vocabularies for the canonical model.

Keep enums small and additive — downstream calc engine pattern-matches on these.
"""
from __future__ import annotations

from enum import Enum


class Country(str, Enum):
    MZ = "MZ"  # Mozambique
    ZA = "ZA"  # South Africa
    MA = "MA"  # Morocco
    EG = "EG"  # Egypt


class Sector(str, Enum):
    ALUMINIUM = "aluminium"
    FERTILISER = "fertiliser"


class SourceMethod(str, Enum):
    """How a data point reached the canonical store."""
    ERP = "ERP"
    METER = "METER"
    INVOICE = "INVOICE"   # OCR'd document
    MANUAL = "MANUAL"
    SUPPLIER = "SUPPLIER"
    CALC = "CALC"


class AluminiumRoute(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    MIX = "mix"


class AnodeType(str, Enum):
    PRE_BAKE = "pre_bake"
    SODERBERG = "soderberg"


class AmmoniaRoute(str, Enum):
    SMR = "SMR"
    ATR = "ATR"
    ELECTROLYSIS = "electrolysis"


class FuelType(str, Enum):
    NATURAL_GAS = "natural_gas"
    DIESEL = "diesel"
    HEAVY_FUEL_OIL = "heavy_fuel_oil"
    LPG = "lpg"
    COAL = "coal"
    COKE = "coke"
    BIOMASS = "biomass"


class MeterType(str, Enum):
    ELECTRICITY_GRID = "electricity_grid"
    ELECTRICITY_SUBPROCESS = "electricity_subprocess"
    NATURAL_GAS = "natural_gas"
    STEAM = "steam"
    SOLAR_PV = "solar_pv"
    DIESEL_GENERATOR = "diesel_generator"
    ANODE_EFFECT = "anode_effect"
    STACK_N2O = "stack_n2o"


class MonitoringMethod(str, Enum):
    TIER1 = "tier1"
    TIER2 = "tier2"
    TIER3 = "tier3"
    CEMS = "cems"
    MASS_BALANCE = "mass_balance"


class GwpSet(str, Enum):
    AR5 = "AR5"
    AR6 = "AR6"


class UnitOfMeasure(str, Enum):
    TONNES = "tonnes"
    KG = "kg"
    LITRES = "litres"
    NM3 = "Nm3"
    KWH = "kWh"
    MWH = "MWh"
    GJ = "GJ"
    EVENTS_PER_POT_DAY = "events_per_pot_day"
    KG_PER_T = "kg_per_t"
    PCT = "pct"


class AllocationMethod(str, Enum):
    """CBAM-permitted coproduct allocation bases."""
    MASS = "mass"
    ENERGY = "energy"
    ECONOMIC = "economic"
    NONE = "none"            # single-product run, no allocation needed


class EFTier(str, Enum):
    """Provenance tier for any emission factor used in the calc engine."""
    MEASURED = "measured"            # CEMS or certified lab
    SUPPLIER_ACTUAL = "supplier_actual"  # 3rd-party verified
    NATIONAL = "national"            # national inventory
    IPCC_DEFAULT = "ipcc_default"
    CBAM_DEFAULT = "cbam_default"
    ESTIMATED = "estimated"          # 20% buffer per CBAM IR Art.4(3)


class SamplingFrequency(str, Enum):
    CONTINUOUS = "continuous"        # CEMS
    DAILY = "daily"
    WEEKLY = "weekly"
    PER_BATCH = "per_batch"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class VerificationOpinion(str, Enum):
    REASONABLE = "reasonable"
    LIMITED = "limited"
    QUALIFIED = "qualified"
    ADVERSE = "adverse"
    NOT_VERIFIED = "not_verified"


class WorkOrderOutcome(str, Enum):
    COMPLETED = "completed"
    REWORK = "rework"
    SCRAP = "scrap"
    QUALITY_HOLD = "quality_hold"
