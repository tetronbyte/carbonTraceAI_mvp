"""Pull canonical CBAM streams from a live ERPNext instance.

Frappe doctype → canonical stream mapping:

  Work Order         → production_runs        (B1.1, B1.5)
  Purchase Order     → purchase_orders        (E1–E5, C1.x for fuels)
  Purchase Invoice   → invoices               (audit + fuel-bill cross-check)
  BOM Item           → bill_of_materials      (B3)
  Sales Invoice      → outbound_shipments     (B1.2 — EU export evidence)

The runner writes JSONL to `data/raw/erpnext/<stream>/<ts>.jsonl` in the *exact
shape* the existing `ErpIngestor` mappers consume — the consumer is unchanged
whether the JSONL came from this runner or from an Airbyte file destination.

Custom Frappe fields the seed script provisions:
  - Item.custom_cn_code           (CBAM CN, 8-digit)
  - Item.custom_facility_code     (e.g. MOZAL-MZ-01)
  - Item.custom_sector            (aluminium | fertiliser)
  - Supplier.custom_country_code  (ISO 2-letter)
  - Work Order.custom_facility_code
  - Work Order.custom_eu_export_share  (0–1)
  - Work Order.custom_scrap_rate_pct
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, Iterable

from src.utils.logger import get_logger
from src.utils.raw_landing import RawLandingZone

from .erpnext_client import ERPNextClient

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# Stream specs — what Frappe fields to fetch + how to flatten to canonical row.
# Each mapper produces a dict with the same keys ErpIngestor's mappers expect.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StreamSpec:
    canonical_stream: str
    doctype: str
    fields: list[str]
    mapper: Callable[[dict[str, Any]], dict[str, Any] | None]
    filters: dict | list | None = None


def _to_iso(v: Any) -> str | None:
    if v is None or v == "":
        return None
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    return str(v)


def _safe_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _map_work_order(doc: dict[str, Any]) -> dict[str, Any] | None:
    """Frappe `Work Order` → production_runs row.

    custom_facility_code, custom_sector, custom_cn_code come from the linked
    Item (we ask ERPNext to hand them back via the fetched-from mechanism on
    the Work Order custom fields). If they're missing we still emit the row
    with sensible defaults — the cleaning layer downstream re-validates.
    """
    qty = _safe_float(doc.get("produced_qty") or doc.get("qty"))
    if qty <= 0:
        return None
    cn = doc.get("custom_cn_code") or doc.get("custom_product_cn_code") or "00000000"
    return {
        "run_id": doc.get("name", ""),
        "facility_id": doc.get("custom_facility_code") or "UNASSIGNED",
        "sector": doc.get("custom_sector") or _sector_from_cn(cn),
        "product_name": doc.get("production_item") or doc.get("product_name") or "unknown",
        "product_cn_code": cn,
        "batch_no": doc.get("name", ""),
        "output_tonnes": qty,
        "scrap_rate_pct": _safe_float(doc.get("custom_scrap_rate_pct")),
        "eu_export_share": _safe_float(doc.get("custom_eu_export_share"), default=0.0),
        "run_started_at": _to_iso(doc.get("actual_start_date") or doc.get("planned_start_date") or doc.get("creation")),
        "run_ended_at": _to_iso(doc.get("actual_end_date") or doc.get("planned_end_date")),
        "shift_supervisor": doc.get("owner") or "",
    }


def _map_purchase_order_item(doc: dict[str, Any]) -> dict[str, Any] | None:
    """`Purchase Order Item` (child) → purchase_orders row."""
    qty = _safe_float(doc.get("qty") or doc.get("stock_qty"))
    if qty <= 0:
        return None
    unit = (doc.get("uom") or doc.get("stock_uom") or "tonnes").lower()
    if unit in ("nos", "unit", "each"):
        unit = "tonnes"  # treated as tonnes for CBAM unless ERP sets a real UoM
    return {
        "po_number": doc.get("parent", ""),
        "facility_id": doc.get("custom_facility_code") or "UNASSIGNED",
        "material_name": (doc.get("item_code") or doc.get("item_name") or "unknown")
                         .lower().replace(" ", "_").replace("-", "_"),
        "material_cn_code": doc.get("custom_cn_code") or "00000000",
        "quantity": qty,
        "unit": unit if unit in ("tonnes", "kg", "litres", "Nm3") else "tonnes",
        "unit_price": _safe_float(doc.get("rate")),
        "currency": "USD",
        "supplier_name": doc.get("custom_supplier_name") or doc.get("supplier") or "unknown",
        "supplier_country": doc.get("custom_supplier_country") or "??",
        "po_date": _to_iso(doc.get("transaction_date") or doc.get("creation")) or date.today().isoformat(),
        "delivery_date": _to_iso(doc.get("schedule_date")) or _to_iso(doc.get("transaction_date")) or date.today().isoformat(),
    }


def _map_bom_item(doc: dict[str, Any]) -> dict[str, Any] | None:
    qty = _safe_float(doc.get("qty"))
    if qty <= 0:
        return None
    return {
        "bom_line_id": doc.get("name", ""),
        "facility_id": doc.get("custom_facility_code") or "UNASSIGNED",
        "product_cn_code": doc.get("custom_product_cn_code") or "00000000",
        "input_material": (doc.get("item_code") or "unknown").lower().replace(" ", "_"),
        "input_cn_code": doc.get("custom_input_cn_code") or "00000000",
        "qty_per_tonne_output": qty,
        "unit": (doc.get("uom") or doc.get("stock_uom") or "tonnes").lower(),
        "recycled_content_pct": _safe_float(doc.get("custom_recycled_content_pct")),
        "effective_from": _to_iso(doc.get("creation")) or date.today().isoformat(),
    }


def _map_purchase_invoice(doc: dict[str, Any]) -> dict[str, Any] | None:
    """`Purchase Invoice` → invoices row (CBAM cost cross-check)."""
    return {
        "invoice_number": doc.get("name", ""),
        "facility_id": doc.get("custom_facility_code") or "UNASSIGNED",
        "vendor_name": doc.get("supplier") or "unknown",
        "invoice_date": _to_iso(doc.get("posting_date")) or date.today().isoformat(),
        "category": doc.get("custom_invoice_category") or "raw_material",
        "quantity": _safe_float(doc.get("total_qty")),
        "unit": "tonnes",
        "unit_price": _safe_float(doc.get("base_grand_total")) / max(_safe_float(doc.get("total_qty"), 1), 1),
        "total_amount": _safe_float(doc.get("base_grand_total")),
        "currency": doc.get("currency") or "USD",
        "po_number": doc.get("custom_po_number") or "",
        "pdf_path": "",
    }


_FUEL_CATEGORIES = {"natural_gas", "diesel", "heavy_fuel_oil", "lpg", "coal", "coke"}


_SECTORS_BY_CN_PREFIX = {
    "76": "aluminium", "28": "fertiliser", "31": "fertiliser",
}


def _sector_from_cn(cn: str) -> str:
    if not cn or len(cn) < 2:
        return "aluminium"
    return _SECTORS_BY_CN_PREFIX.get(cn[:2], "aluminium")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

class ERPNextRunner:
    """Pulls all CBAM-relevant streams from ERPNext into the JSONL landing zone.

    Returns a `{stream_name: jsonl_path}` map so the caller can hand each path
    to an `ErpIngestor` instance (one per stream).
    """

    STREAM_SPECS: tuple[StreamSpec, ...] = (
        StreamSpec(
            canonical_stream="production_runs",
            doctype="Work Order",
            fields=[
                "name", "production_item", "qty", "produced_qty",
                "planned_start_date", "planned_end_date",
                "actual_start_date", "actual_end_date",
                "creation", "owner", "status",
                "custom_facility_code", "custom_sector", "custom_cn_code",
                "custom_eu_export_share", "custom_scrap_rate_pct",
            ],
            mapper=_map_work_order,
            filters={"docstatus": ["!=", 2]},
        ),
        StreamSpec(
            canonical_stream="purchase_orders",
            doctype="Purchase Order Item",
            fields=[
                "name", "parent", "item_code", "item_name",
                "qty", "stock_qty", "uom", "stock_uom", "rate",
                "schedule_date", "creation",
                "custom_facility_code", "custom_cn_code",
                "custom_supplier_name", "custom_supplier_country",
                "transaction_date",
            ],
            mapper=_map_purchase_order_item,
        ),
        StreamSpec(
            canonical_stream="bill_of_materials",
            doctype="BOM Item",
            fields=[
                "name", "parent", "item_code", "qty", "uom", "stock_uom",
                "creation",
                "custom_facility_code", "custom_product_cn_code",
                "custom_input_cn_code", "custom_recycled_content_pct",
            ],
            mapper=_map_bom_item,
        ),
        StreamSpec(
            canonical_stream="invoices",
            doctype="Purchase Invoice",
            fields=[
                "name", "supplier", "posting_date", "total_qty",
                "base_grand_total", "currency",
                "custom_facility_code", "custom_invoice_category",
                "custom_po_number",
            ],
            mapper=_map_purchase_invoice,
            filters={"docstatus": 1},
        ),
    )

    def __init__(self, client: ERPNextClient, page_size: int = 200) -> None:
        self.client = client
        self.page_size = page_size

    def sync_all(self) -> dict[str, Path]:
        out: dict[str, Path] = {}
        for spec in self.STREAM_SPECS:
            out[spec.canonical_stream] = self._sync_stream(spec)
        return out

    def _sync_stream(self, spec: StreamSpec) -> Path:
        landing = RawLandingZone(source="erpnext", stream=spec.canonical_stream)
        log.info("ERPNext: pulling %s -> %s", spec.doctype, landing.path)

        rows_in = rows_written = 0
        with landing.open() as writer:
            for raw in self.client.iter_all(
                spec.doctype,
                fields=spec.fields,
                filters=spec.filters,
                page_size=self.page_size,
            ):
                rows_in += 1
                row = spec.mapper(raw)
                if row is None:
                    continue
                writer.write(row)
                rows_written += 1
        log.info("ERPNext: %s — pulled=%s, written=%s", spec.doctype, rows_in, rows_written)
        return landing.path
