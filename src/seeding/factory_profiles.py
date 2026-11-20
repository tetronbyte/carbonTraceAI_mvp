"""Two CBAM-relevant factory profiles for the demo.

Each profile describes a mid/large plant in enough detail that the synthetic
data set we inject into ERPNext is coherent (real CN codes, real precursor
suppliers, plausible BOM ratios, plausible monthly output).

The seeder reads these structures and writes the corresponding Items,
Suppliers, Customers, BOMs, Work Orders, Purchase Orders, and Purchase
Invoices to ERPNext via the REST API.

References:
  - CBAM Implementing Reg 2023/1773 Annex II (aluminium) & Annex V (fertilisers)
  - IPCC 2006 Vol 3 Ch 4 (metals) & Vol 3 Ch 3 (chemicals)
  - Public reports: Mozal SA, South32 Hillside, OCP Group, Abu Qir Fertilisers
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class ItemSpec:
    item_code: str
    item_name: str
    cn_code: str            # 8-digit CBAM CN
    item_group: str         # e.g. raw_material, fuel, finished_good
    uom: str                # tonnes, Nm3, litres, kWh
    is_finished: bool = False
    recycled_content_pct: float = 0.0


@dataclass(frozen=True)
class SupplierSpec:
    supplier_name: str
    country: str            # ISO 2
    supplier_group: str = "Raw Material"
    sells_items: tuple[str, ...] = ()   # item_codes


@dataclass(frozen=True)
class BomLine:
    input_item: str
    qty_per_tonne_output: float
    uom: str
    recycled_content_pct: float = 0.0


@dataclass(frozen=True)
class FinishedProduct:
    item_code: str
    monthly_output_tonnes_mean: float
    monthly_output_tonnes_sigma: float
    eu_export_share_mean: float          # 0–1 — fraction of output shipped to EU
    bom: tuple[BomLine, ...]


@dataclass(frozen=True)
class FactoryProfile:
    key: str
    facility_code: str
    sector: Literal["aluminium", "fertiliser"]
    legal_name: str
    plant_name: str
    country: str
    currency: str
    electricity_supplier: str            # for the manual sensor / supplier portal flows
    grid_ef_kgco2_per_kwh: float
    # Synthetic site electricity intensity. ERPNext holds no meter data, so the
    # demo meter reading is sized from this and the quarter's output.
    electricity_kwh_per_tonne: float
    items: tuple[ItemSpec, ...]
    suppliers: tuple[SupplierSpec, ...]
    eu_customers: tuple[SupplierSpec, ...]
    products: tuple[FinishedProduct, ...]
    months: int = 24                     # months of history to seed
    work_orders_per_month: int = 60
    purchase_orders_per_month: int = 40

    # ---- seeder v2 additions ----
    # Monthly seasonality multipliers (length 12, Jan→Dec) applied to output.
    # Aluminium: stable year-round; Fertiliser: NPK demand cycle, lower in Q3.
    seasonality: tuple[float, ...] = (1.0,) * 12
    # Annual planned-shutdown windows: [(start_month, duration_days, severity)]
    # severity = output factor during the window (e.g. 0.10 = 10% normal output)
    shutdowns: tuple[tuple[int, int, float], ...] = ()
    # Failure rate (fraction of work orders that go to rework / scrap)
    rework_rate: float = 0.015
    scrap_rate: float = 0.005
    # Cost centres for sub-process electricity allocation (Block C2.2)
    cost_centres: tuple[str, ...] = ("site_total",)
    # Monthly price drift — annualised standard deviation of unit_price
    price_drift_sigma: float = 0.04

    # EORI / UN-LOCODE / CBAM installation ID — Section 1 & 3
    eori: str = ""
    un_locode: str = ""
    cbam_installation_id: str = ""


# =========================================================================
# MOZAL ALUMINIUM — Mozambique
# =========================================================================
MOZAL_ALUMINIUM = FactoryProfile(
    key="mozal_aluminium",
    facility_code="MOZAL-MZ-01",
    sector="aluminium",
    legal_name="Mozal SA",
    plant_name="Mozal Aluminium Smelter",
    country="MZ",
    currency="USD",
    electricity_supplier="EDM",
    grid_ef_kgco2_per_kwh=0.04,         # hydro-dominated
    electricity_kwh_per_tonne=14_500,   # typical Hall-Heroult smelter, demo value
    items=(
        # finished goods
        ItemSpec("AL-INGOT-P1020",  "Primary Aluminium Ingot P1020",       "76011000", "finished_good", "tonnes", is_finished=True),
        ItemSpec("AL-SLAB-2050",    "Primary Aluminium Slab 2050",          "76011000", "finished_good", "tonnes", is_finished=True),
        # raw / precursor materials
        ItemSpec("ALUMINA-SG",      "Smelter-Grade Alumina (Al2O3)",        "28182000", "raw_material",  "tonnes"),
        ItemSpec("ANODE-PREBAKE",   "Pre-bake Carbon Anode Block",          "38011000", "raw_material",  "tonnes"),
        ItemSpec("ALF3",            "Aluminium Fluoride",                   "28261200", "raw_material",  "tonnes"),
        ItemSpec("CRYOLITE",        "Synthetic Cryolite (Na3AlF6)",         "28261910", "raw_material",  "tonnes"),
        ItemSpec("ANODE-BUTT",      "Spent Anode Butt (recycled)",          "38011000", "raw_material",  "tonnes", recycled_content_pct=100),
        # fuels / utilities
        ItemSpec("DIESEL",          "Diesel — generators & casthouse",      "27101941", "fuel",          "litres"),
        ItemSpec("NAT-GAS",         "Natural gas — casthouse furnaces",     "27112100", "fuel",          "Nm3"),
        ItemSpec("LPG",             "LPG",                                  "27111200", "fuel",          "kg"),
    ),
    suppliers=(
        SupplierSpec("Alunorte Refinery",      "BR", sells_items=("ALUMINA-SG",)),
        SupplierSpec("Worsley Alumina",        "AU", sells_items=("ALUMINA-SG",)),
        SupplierSpec("Rio Tinto Yarwun",       "AU", sells_items=("ALUMINA-SG",)),
        SupplierSpec("UC Rusal Aughinish",     "IE", sells_items=("ALUMINA-SG",)),
        SupplierSpec("Aluchemie Anodes",       "NL", sells_items=("ANODE-PREBAKE",)),
        SupplierSpec("R&D Carbon Anodes",      "CN", sells_items=("ANODE-PREBAKE",)),
        SupplierSpec("Fluorsid SpA",           "IT", sells_items=("ALF3",)),
        SupplierSpec("Tanfac Industries",      "IN", sells_items=("ALF3", "CRYOLITE")),
        SupplierSpec("Sasol Energy",           "ZA", sells_items=("DIESEL", "LPG"), supplier_group="Energy"),
        SupplierSpec("Sasol Gas",              "ZA", sells_items=("NAT-GAS",), supplier_group="Energy"),
    ),
    eu_customers=(
        SupplierSpec("Norsk Hydro",            "NO", supplier_group="Customer"),
        SupplierSpec("Speira GmbH",            "DE", supplier_group="Customer"),
        SupplierSpec("Trimet Aluminium",       "DE", supplier_group="Customer"),
        SupplierSpec("Aluminium Dunkerque",    "FR", supplier_group="Customer"),
        SupplierSpec("Aleris Rolled Products", "BE", supplier_group="Customer"),
    ),
    products=(
        FinishedProduct(
            item_code="AL-INGOT-P1020",
            monthly_output_tonnes_mean=44_000,         # ~530 kt/yr design capacity
            monthly_output_tonnes_sigma=3_000,
            eu_export_share_mean=0.62,                  # Mozal exports majority to EU
            bom=(
                BomLine("ALUMINA-SG",   1.925, "tonnes"),
                BomLine("ANODE-PREBAKE", 0.43, "tonnes"),
                BomLine("ALF3",          0.018, "tonnes"),
                BomLine("CRYOLITE",      0.005, "tonnes"),
            ),
        ),
        FinishedProduct(
            item_code="AL-SLAB-2050",
            monthly_output_tonnes_mean=4_000,
            monthly_output_tonnes_sigma=600,
            eu_export_share_mean=0.55,
            bom=(
                BomLine("ALUMINA-SG",   1.92, "tonnes"),
                BomLine("ANODE-PREBAKE", 0.42, "tonnes"),
                BomLine("ALF3",          0.018, "tonnes"),
            ),
        ),
    ),
    months=24,
    work_orders_per_month=60,
    purchase_orders_per_month=40,
    # Aluminium smelters run essentially flat; small Aug maintenance dip
    seasonality=(1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
                 1.00, 0.85, 1.00, 1.00, 1.00, 1.00),
    shutdowns=((8, 12, 0.40),),                      # mid-Aug 12-day partial shutdown
    rework_rate=0.012,
    scrap_rate=0.004,
    cost_centres=("potline_1", "potline_2", "anode_plant", "casthouse", "utilities"),
    price_drift_sigma=0.05,
    eori="MZ100123456789",                           # mock — assigned by EU declarant
    un_locode="MZMPM",                               # Maputo
    cbam_installation_id="MZ-INST-001",
)


# =========================================================================
# OCP JORF LASFAR — Morocco (fertiliser)
# =========================================================================
OCP_FERTILISER = FactoryProfile(
    key="ocp_fertiliser",
    facility_code="OCPJORF-MA-01",
    sector="fertiliser",
    legal_name="OCP SA",
    plant_name="OCP Jorf Lasfar — Fertiliser & Ammonia Trains",
    country="MA",
    currency="USD",
    electricity_supplier="ONEE",
    grid_ef_kgco2_per_kwh=0.62,
    electricity_kwh_per_tonne=150,      # blended fertiliser site, demo value
    items=(
        # finished goods
        ItemSpec("AMMONIA-ANH",     "Anhydrous Ammonia (NH3)",              "28141000", "finished_good", "tonnes", is_finished=True),
        ItemSpec("UREA-PRILLED",    "Prilled Urea (46% N)",                 "31021010", "finished_good", "tonnes", is_finished=True),
        ItemSpec("DAP-FERT",        "Di-ammonium Phosphate (DAP)",          "31053000", "finished_good", "tonnes", is_finished=True),
        ItemSpec("HNO3-58",         "Nitric Acid (58%)",                    "28080000", "finished_good", "tonnes", is_finished=True),
        # raw / precursor
        ItemSpec("PHOS-ROCK",       "Phosphate rock — local OCP mine",      "25101000", "raw_material",  "tonnes"),
        ItemSpec("POTASH-KCL",      "Potassium chloride (potash)",          "31042000", "raw_material",  "tonnes"),
        ItemSpec("SULPHUR-EL",      "Elemental sulphur",                    "25030000", "raw_material",  "tonnes"),
        ItemSpec("CO2-CAPT",        "Captured CO2 (urea synthesis)",        "28112100", "raw_material",  "tonnes"),
        # fuels — natural gas is FEEDSTOCK + fuel for SMR
        ItemSpec("NAT-GAS-FS",      "Natural gas — SMR feedstock",          "27112100", "feedstock",     "Nm3"),
        ItemSpec("NAT-GAS-FUEL",   "Natural gas — process heat",            "27112100", "fuel",          "Nm3"),
        ItemSpec("HFO",             "Heavy fuel oil",                        "27101962", "fuel",          "tonnes"),
        ItemSpec("DIESEL",          "Diesel — site fleet",                  "27101941", "fuel",          "litres"),
    ),
    suppliers=(
        SupplierSpec("OCP Khouribga Mine",     "MA", sells_items=("PHOS-ROCK",)),
        SupplierSpec("Uralkali",               "RU", sells_items=("POTASH-KCL",)),
        SupplierSpec("ICL Israel",             "IL", sells_items=("POTASH-KCL",)),
        SupplierSpec("Belaruskali",            "BY", sells_items=("POTASH-KCL",)),
        SupplierSpec("Mosaic Company",         "US", sells_items=("SULPHUR-EL",)),
        SupplierSpec("Tasweeq Qatar",          "QA", sells_items=("SULPHUR-EL",)),
        SupplierSpec("Qatargas LNG",           "QA", sells_items=("NAT-GAS-FS", "NAT-GAS-FUEL"), supplier_group="Energy"),
        SupplierSpec("Sonatrach",              "DZ", sells_items=("NAT-GAS-FS", "NAT-GAS-FUEL"), supplier_group="Energy"),
        SupplierSpec("Vitol SA",               "CH", sells_items=("HFO", "DIESEL"), supplier_group="Energy"),
    ),
    eu_customers=(
        SupplierSpec("Yara International",     "NO", supplier_group="Customer"),
        SupplierSpec("Borealis AG",            "AT", supplier_group="Customer"),
        SupplierSpec("Eurochem Antwerpen",     "BE", supplier_group="Customer"),
        SupplierSpec("ICL Iberia",             "ES", supplier_group="Customer"),
        SupplierSpec("Grupa Azoty",            "PL", supplier_group="Customer"),
    ),
    products=(
        FinishedProduct(
            item_code="AMMONIA-ANH",
            monthly_output_tonnes_mean=80_000,
            monthly_output_tonnes_sigma=4_500,
            eu_export_share_mean=0.35,
            bom=(
                BomLine("NAT-GAS-FS",   850, "Nm3"),            # ~31 GJ feedstock/t NH3
                BomLine("NAT-GAS-FUEL", 320, "Nm3"),
            ),
        ),
        FinishedProduct(
            item_code="UREA-PRILLED",
            monthly_output_tonnes_mean=120_000,
            monthly_output_tonnes_sigma=8_000,
            eu_export_share_mean=0.55,
            bom=(
                BomLine("AMMONIA-ANH", 0.58, "tonnes"),
                BomLine("CO2-CAPT",    0.78, "tonnes"),
                BomLine("NAT-GAS-FUEL", 90, "Nm3"),
            ),
        ),
        FinishedProduct(
            item_code="DAP-FERT",
            monthly_output_tonnes_mean=180_000,
            monthly_output_tonnes_sigma=15_000,
            eu_export_share_mean=0.42,
            bom=(
                BomLine("PHOS-ROCK",   3.20, "tonnes"),
                BomLine("SULPHUR-EL",  0.40, "tonnes"),
                BomLine("AMMONIA-ANH", 0.22, "tonnes"),
            ),
        ),
        FinishedProduct(
            item_code="HNO3-58",
            monthly_output_tonnes_mean=22_000,
            monthly_output_tonnes_sigma=1_800,
            eu_export_share_mean=0.20,
            bom=(
                BomLine("AMMONIA-ANH", 0.28, "tonnes"),
            ),
        ),
    ),
    months=24,
    work_orders_per_month=70,
    purchase_orders_per_month=50,
    # NPK fertiliser cycle: planting peaks in N-hemisphere spring (Mar–May) +
    # autumn (Sep–Oct); slow July/August.
    seasonality=(0.95, 1.05, 1.15, 1.20, 1.10, 0.90,
                 0.75, 0.80, 1.10, 1.20, 1.05, 0.85),
    shutdowns=((7, 18, 0.30),),                      # July 18-day turnaround
    rework_rate=0.018,
    scrap_rate=0.006,
    cost_centres=("smr_unit", "urea_unit", "nitric_acid_unit", "dap_unit", "utilities"),
    price_drift_sigma=0.06,
    eori="MA200456789012",
    un_locode="MAJEN",                               # Jorf Lasfar
    cbam_installation_id="MA-INST-008",
)


PROFILES: dict[str, FactoryProfile] = {
    MOZAL_ALUMINIUM.key: MOZAL_ALUMINIUM,
    OCP_FERTILISER.key: OCP_FERTILISER,
}


def get_profile(key: str) -> FactoryProfile:
    if key not in PROFILES:
        raise KeyError(f"Unknown factory profile {key!r}. Known: {list(PROFILES)}")
    return PROFILES[key]
