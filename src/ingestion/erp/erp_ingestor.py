"""ERP ingestor — reads JSONL landings from `data/raw/erp/<stream>/` and maps
each row into one or more canonical Pydantic models.

One ingestor instance handles one stream. Swap the producer (direct ERPNext
REST runner vs. Airbyte file destination) — this consumer doesn't change.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from pydantic import BaseModel

from src.core.base import BaseIngestor
from src.core.enums import (
    AluminiumRoute,
    FuelType,
    MeterType,
    Sector,
    SourceMethod,
    UnitOfMeasure,
)
from src.core.models import (
    EnergyConsumption,
    GLEntry,
    OutboundShipment,
    PrecursorPurchase,
    ProductionRun,
    StockMovement,
)
from src.utils.logger import get_logger

log = get_logger(__name__)


# Mapping helpers — kept module-level so the calc engine can reuse them later.
_PRECURSOR_MATERIALS = {
    "alumina", "carbon_anode_block", "aluminium_fluoride", "aluminium_scrap",
    "phosphate_rock", "potash", "sulphur", "limestone",
    # ERPNext item codes after the runner normalises them (factory_profiles.py)
    "alumina_sg", "anode_prebake", "alf3", "cryolite",
    "phos_rock", "potash_kcl", "sulphur_el",
}

_FUEL_TO_METER = {
    "natural_gas": (MeterType.NATURAL_GAS, UnitOfMeasure.NM3, FuelType.NATURAL_GAS),
    "diesel": (MeterType.DIESEL_GENERATOR, UnitOfMeasure.LITRES, FuelType.DIESEL),
    "heavy_fuel_oil": (MeterType.DIESEL_GENERATOR, UnitOfMeasure.LITRES, FuelType.HEAVY_FUEL_OIL),
    # ERPNext item codes. NAT-GAS-FS is excluded on purpose: feedstock gas is
    # counted as process CO2 through FertiliserProcessRecord, not as combustion.
    "nat_gas": (MeterType.NATURAL_GAS, UnitOfMeasure.NM3, FuelType.NATURAL_GAS),
    "nat_gas_fuel": (MeterType.NATURAL_GAS, UnitOfMeasure.NM3, FuelType.NATURAL_GAS),
    "hfo": (MeterType.DIESEL_GENERATOR, UnitOfMeasure.TONNES, FuelType.HEAVY_FUEL_OIL),
}

_METER_TYPE_MAP = {
    "electricity_grid": MeterType.ELECTRICITY_GRID,
    "electricity_subprocess": MeterType.ELECTRICITY_SUBPROCESS,
    "natural_gas": MeterType.NATURAL_GAS,
    "steam": MeterType.STEAM,
    "solar_pv": MeterType.SOLAR_PV,
    "diesel_generator": MeterType.DIESEL_GENERATOR,
    "anode_effect": MeterType.ANODE_EFFECT,
    "stack_n2o": MeterType.STACK_N2O,
}

_UNIT_MAP = {
    "kWh": UnitOfMeasure.KWH, "Nm3": UnitOfMeasure.NM3, "GJ": UnitOfMeasure.GJ,
    "litres": UnitOfMeasure.LITRES, "tonnes": UnitOfMeasure.TONNES, "kg": UnitOfMeasure.KG,
    "events_per_pot_day": UnitOfMeasure.EVENTS_PER_POT_DAY, "kg_per_t": UnitOfMeasure.KG_PER_T,
}

_SECTOR_BY_CN = {
    "76011000": Sector.ALUMINIUM, "76012000": Sector.ALUMINIUM,
    "28141000": Sector.FERTILISER, "31021010": Sector.FERTILISER, "28080000": Sector.FERTILISER,
}


class ErpIngestor(BaseIngestor):
    source = SourceMethod.ERP

    # one ingestor per stream — `stream` set per instance
    def __init__(
        self,
        repository: Any,
        *,
        stream: str,
        landing_path: Path,
        mapper: Callable[[dict[str, Any], str], Sequence[BaseModel]] | None = None,
    ) -> None:
        self.stream = stream
        super().__init__(repository, raw_path=str(landing_path))
        self.landing_path = Path(landing_path)
        self._mapper = mapper or _default_mapper_for(stream)

    def fetch(self, **_: Any) -> Iterable[dict[str, Any]]:
        if not self.landing_path.exists():
            log.warning("Landing missing for stream %s at %s", self.stream, self.landing_path)
            return
        with self.landing_path.open() as fh:
            for i, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                row.setdefault("_raw_ref", f"{self.landing_path}:{i}")
                yield row

    def map(self, raw: dict[str, Any]) -> Sequence[BaseModel]:
        return self._mapper(raw, raw.get("_raw_ref", ""))


# ---------- default mappers per stream ----------
def _default_mapper_for(stream: str) -> Callable[[dict[str, Any], str], Sequence[BaseModel]]:
    return {
        "production_runs": _map_production_run,
        "purchase_orders": _map_purchase_order,
        "energy_meter_readings": _map_meter_reading,
        "stock_movements": _map_stock_movement,
        "gl_entries": _map_gl_entry_row,
        "outbound_shipments": _map_outbound_shipment,
        # invoices and bom flow through OCR ingestor / future BOM mapper respectively
    }.get(stream, _noop_mapper)


def _map_stock_movement(raw: dict[str, Any], ref: str) -> Sequence[BaseModel]:
    unit_str = raw.get("unit", "tonnes")
    try:
        unit = UnitOfMeasure(unit_str)
    except ValueError:
        unit = UnitOfMeasure.TONNES
    return [StockMovement(
        source=SourceMethod.ERP, raw_ref=ref,
        facility_id=raw.get("facility_id", "UNASSIGNED"),
        movement_date=raw["movement_date"],
        item_code=raw.get("item_code", "unknown"),
        item_cn_code=raw.get("item_cn_code"),
        qty=float(raw["qty"]),
        unit=unit,
        movement_type=raw.get("movement_type", "receive"),
        work_order_id=raw.get("work_order_id"),
        purchase_order_id=raw.get("purchase_order_id"),
        cost_centre=raw.get("cost_centre"),
    )]


def _map_gl_entry_row(raw: dict[str, Any], ref: str) -> Sequence[BaseModel]:
    return [GLEntry(
        source=SourceMethod.ERP, raw_ref=ref,
        facility_id=raw.get("facility_id", "UNASSIGNED"),
        posting_date=raw["posting_date"],
        voucher_type=raw.get("voucher_type", "Journal Entry"),
        voucher_no=raw.get("voucher_no", ""),
        account=raw.get("account", ""),
        debit_local=float(raw.get("debit_local", 0)),
        credit_local=float(raw.get("credit_local", 0)),
        currency=raw.get("currency", "USD"),
        cost_centre=raw.get("cost_centre"),
        against_item_code=raw.get("against_item_code"),
    )]


def _map_outbound_shipment(raw: dict[str, Any], ref: str) -> Sequence[BaseModel]:
    return [OutboundShipment(
        source=SourceMethod.ERP, raw_ref=ref,
        facility_id=raw.get("facility_id", "UNASSIGNED"),
        shipment_date=raw["shipment_date"],
        port_of_loading=raw.get("port_of_loading", "UNKNOWN"),
        port_of_discharge=raw.get("port_of_discharge", "UNKNOWN"),
        vessel_name=raw.get("vessel_name"),
        cargo_tonnes=float(raw.get("cargo_tonnes", 0)),
        cn_code=raw.get("cn_code", "00000000"),
        sea_distance_nm=raw.get("sea_distance_nm"),
        bill_of_lading_path=raw.get("bill_of_lading_path"),
        eu_importer_name=raw.get("eu_importer_name"),
        customs_invoice_value_eur=raw.get("customs_invoice_value_eur"),
    )]


def _noop_mapper(_raw: dict[str, Any], _ref: str) -> Sequence[BaseModel]:
    return []


def _map_production_run(raw: dict[str, Any], ref: str) -> Sequence[BaseModel]:
    cn = raw["product_cn_code"]
    sector = _SECTOR_BY_CN.get(cn, Sector(raw.get("sector", "aluminium")))
    output_t = float(raw["output_tonnes"])
    eu_share = float(raw.get("eu_export_share", 0) or 0)
    return [
        ProductionRun(
            source=SourceMethod.ERP,
            raw_ref=ref,
            facility_id=raw["facility_id"],
            sector=sector,
            product_name=raw.get("product_name", "unknown"),
            product_cn_code=cn,
            batch_run_id=raw.get("batch_no") or raw["run_id"],
            output_tonnes=output_t,
            eu_export_tonnes=round(output_t * max(0.0, min(1.0, eu_share)), 4),
            domestic_sales_tonnes=round(output_t * (1 - max(0.0, min(1.0, eu_share))), 4),
            scrap_rate_pct=raw.get("scrap_rate_pct", 0),
            aluminium_route=AluminiumRoute.PRIMARY if sector == Sector.ALUMINIUM and "primary" in raw.get("product_name", "") else None,
            run_started_at=_to_dt(raw["run_started_at"]),
            run_ended_at=_to_dt(raw.get("run_ended_at")),
        )
    ]


def _map_purchase_order(raw: dict[str, Any], ref: str) -> Sequence[BaseModel]:
    material = raw["material_name"]
    qty = float(raw["quantity"])
    purchase_date = _to_date(raw["po_date"])

    # Precursor materials → PrecursorPurchase (Block E)
    if material in _PRECURSOR_MATERIALS:
        return [
            PrecursorPurchase(
                source=SourceMethod.ERP,
                raw_ref=ref,
                facility_id=raw["facility_id"],
                po_number=raw.get("po_number"),
                precursor_name=material,
                precursor_cn_code=raw.get("material_cn_code", "00000000"),
                quantity_tonnes=qty if raw.get("unit") == "tonnes" else qty / 1000,
                supplier_name=raw.get("supplier_name", "unknown"),
                supplier_country=raw.get("supplier_country"),
                purchase_date=purchase_date,
                ee_method="default",  # supplier portal will overwrite later
            )
        ]

    # Fuel purchases → EnergyConsumption (Block C, Scope 1)
    if material in _FUEL_TO_METER:
        meter_type, unit, fuel = _FUEL_TO_METER[material]
        return [
            EnergyConsumption(
                source=SourceMethod.ERP,
                raw_ref=ref,
                facility_id=raw["facility_id"],
                period_start=purchase_date,
                period_end=purchase_date,
                meter_type=meter_type,
                quantity=qty,
                unit=unit,
                fuel_type=fuel,
                supplier_name=raw.get("supplier_name"),
                quality_flag="ok",
            )
        ]
    log.warning("PO %s: material %r is neither a precursor nor a fuel; no emissions row created",
                raw.get("po_number"), material)
    return []


def _map_meter_reading(raw: dict[str, Any], ref: str) -> Sequence[BaseModel]:
    meter_type = _METER_TYPE_MAP.get(raw["meter_type"])
    unit = _UNIT_MAP.get(raw.get("unit", "kWh"), UnitOfMeasure.KWH)
    if not meter_type:
        return []
    reading_at = _to_dt(raw["reading_at"]).date()
    return [
        EnergyConsumption(
            source=SourceMethod.METER,
            raw_ref=ref,
            facility_id=raw["facility_id"],
            period_start=reading_at,
            period_end=reading_at,
            meter_type=meter_type,
            meter_id=raw.get("meter_id"),
            cost_centre=raw.get("cost_centre"),
            quantity=float(raw["value"]),
            unit=unit,
            quality_flag=raw.get("quality_flag", "ok"),
        )
    ]


def _to_dt(v: Any) -> datetime:
    if isinstance(v, datetime):
        return v
    return datetime.fromisoformat(str(v).replace("Z", "+00:00"))


def _to_date(v: Any) -> date:
    if isinstance(v, date):
        return v
    return date.fromisoformat(str(v))
