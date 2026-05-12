"""Injects a FactoryProfile into an ERPNext sandbox.

Sequence:
  1. Provision the carbonTraceAI custom fields on Item, Supplier, Work Order,
     BOM Item, and Purchase Invoice (CN code, facility code, etc.).
  2. Upsert UOMs, Item Groups, Items, Suppliers, Customers.
  3. For each FinishedProduct → create the BOM.
  4. For `months` × `work_orders_per_month` → create Work Orders with realistic
     timestamps, output qty (normal-distributed around the profile mean),
     `custom_eu_export_share`, `custom_scrap_rate_pct`.
  5. For `months` × `purchase_orders_per_month` → create Purchase Orders with a
     supplier sampled weighted by which items they sell.
  6. Optionally create Purchase Invoices for a fraction of POs.

All writes go through `ERPNextClient.upsert` / `.insert`, so re-running the
seed is idempotent on Items / Suppliers / Customers / BOM / custom fields and
purely additive on transactional docs.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any

from src.core.exceptions import IngestionError
from src.ingestion.erp.erpnext_client import ERPNextClient
from src.utils.logger import get_logger

from .factory_profiles import FactoryProfile, FinishedProduct, ItemSpec, SupplierSpec

log = get_logger(__name__)


# --------------------------------------------------------------------------
# Custom field definitions — CBAM-specific fields the seeder injects.
# --------------------------------------------------------------------------
_CUSTOM_FIELDS: list[dict[str, Any]] = [
    # Item
    {"dt": "Item", "fieldname": "custom_cn_code",            "label": "CBAM CN Code",          "fieldtype": "Data",  "insert_after": "item_group"},
    {"dt": "Item", "fieldname": "custom_facility_code",      "label": "Facility Code",         "fieldtype": "Data",  "insert_after": "custom_cn_code"},
    {"dt": "Item", "fieldname": "custom_sector",             "label": "CBAM Sector",            "fieldtype": "Select", "options": "\naluminium\nfertiliser", "insert_after": "custom_facility_code"},
    {"dt": "Item", "fieldname": "custom_recycled_content_pct","label": "Recycled Content (%)", "fieldtype": "Float", "insert_after": "custom_sector"},
    # Supplier
    {"dt": "Supplier", "fieldname": "custom_country_code",   "label": "ISO Country Code",      "fieldtype": "Data",  "insert_after": "country"},
    # Work Order
    {"dt": "Work Order", "fieldname": "custom_facility_code",     "label": "Facility Code",        "fieldtype": "Data",  "insert_after": "production_item"},
    {"dt": "Work Order", "fieldname": "custom_sector",            "label": "CBAM Sector",          "fieldtype": "Select", "options": "\naluminium\nfertiliser", "insert_after": "custom_facility_code"},
    {"dt": "Work Order", "fieldname": "custom_cn_code",           "label": "Product CN Code",      "fieldtype": "Data",  "insert_after": "custom_sector"},
    {"dt": "Work Order", "fieldname": "custom_eu_export_share",   "label": "EU Export Share",      "fieldtype": "Float", "insert_after": "custom_cn_code"},
    {"dt": "Work Order", "fieldname": "custom_scrap_rate_pct",    "label": "Scrap Rate (%)",       "fieldtype": "Float", "insert_after": "custom_eu_export_share"},
    # BOM Item
    {"dt": "BOM Item", "fieldname": "custom_facility_code",       "label": "Facility Code",        "fieldtype": "Data",  "insert_after": "item_code"},
    {"dt": "BOM Item", "fieldname": "custom_product_cn_code",     "label": "Product CN",           "fieldtype": "Data",  "insert_after": "custom_facility_code"},
    {"dt": "BOM Item", "fieldname": "custom_input_cn_code",       "label": "Input CN",             "fieldtype": "Data",  "insert_after": "custom_product_cn_code"},
    {"dt": "BOM Item", "fieldname": "custom_recycled_content_pct","label": "Recycled Content (%)", "fieldtype": "Float", "insert_after": "custom_input_cn_code"},
    # Purchase Order Item
    {"dt": "Purchase Order Item", "fieldname": "custom_facility_code",    "label": "Facility Code",     "fieldtype": "Data", "insert_after": "item_code"},
    {"dt": "Purchase Order Item", "fieldname": "custom_cn_code",          "label": "CBAM CN",           "fieldtype": "Data", "insert_after": "custom_facility_code"},
    {"dt": "Purchase Order Item", "fieldname": "custom_supplier_name",    "label": "Supplier Name",     "fieldtype": "Data", "insert_after": "custom_cn_code"},
    {"dt": "Purchase Order Item", "fieldname": "custom_supplier_country", "label": "Supplier Country",  "fieldtype": "Data", "insert_after": "custom_supplier_name"},
    # Purchase Invoice
    {"dt": "Purchase Invoice", "fieldname": "custom_facility_code",       "label": "Facility Code",     "fieldtype": "Data", "insert_after": "supplier"},
    {"dt": "Purchase Invoice", "fieldname": "custom_invoice_category",    "label": "CBAM Category",     "fieldtype": "Select", "options": "\nraw_material\nfuel\nelectricity\nnatural_gas\ndiesel\nlogistics\nother", "insert_after": "custom_facility_code"},
    {"dt": "Purchase Invoice", "fieldname": "custom_po_number",           "label": "Linked PO",         "fieldtype": "Data", "insert_after": "custom_invoice_category"},
]


@dataclass
class SeedReport:
    profile_key: str
    custom_fields: int = 0
    items: int = 0
    suppliers: int = 0
    customers: int = 0
    cost_centres: int = 0
    boms: int = 0
    work_orders: int = 0
    rework_orders: int = 0
    purchase_orders: int = 0
    purchase_invoices: int = 0
    stock_entries: int = 0
    quality_inspections: int = 0
    sales_invoices: int = 0
    errors: list[str] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"[seed:{self.profile_key}] "
            f"items={self.items} suppliers={self.suppliers} customers={self.customers} "
            f"cost_centres={self.cost_centres} boms={self.boms} "
            f"wo={self.work_orders} rework={self.rework_orders} "
            f"po={self.purchase_orders} pinv={self.purchase_invoices} "
            f"stock={self.stock_entries} qa={self.quality_inspections} "
            f"sinv={self.sales_invoices} errors={len(self.errors)}"
        )


class ERPNextSeeder:
    """Idempotent seeder. Re-running it on the same profile is safe."""

    def __init__(
        self,
        client: ERPNextClient,
        profile: FactoryProfile,
        *,
        seed: int = 42,
        invoice_ratio: float = 0.6,
    ) -> None:
        self.client = client
        self.profile = profile
        self.rand = random.Random(seed)
        self.invoice_ratio = invoice_ratio
        self.report = SeedReport(profile_key=profile.key)

    # ---- public ----
    def run(self) -> SeedReport:
        log.info("Seeding ERPNext with profile %s", self.profile.key)
        self._provision_custom_fields()
        self._provision_uoms()
        self._provision_item_groups()
        self._provision_items()
        self._provision_suppliers()
        self._provision_customers()
        self._provision_cost_centres()       # NEW v2
        self._provision_boms()
        # Stoichiometric driver: planned monthly outputs first, then POs sized
        # from BOM ratios with a ±5% noise band. Mass-balance coherent.
        monthly_plans = self._build_monthly_plans()
        self._generate_work_orders(monthly_plans)
        self._generate_purchase_orders(monthly_plans)
        self._generate_sales_invoices(monthly_plans)
        log.info(self.report.summary())
        return self.report

    # ---- custom fields -------------------------------------------------------
    def _provision_custom_fields(self) -> None:
        for cf in _CUSTOM_FIELDS:
            try:
                self.client.insert("Custom Field", {
                    "dt": cf["dt"],
                    "fieldname": cf["fieldname"],
                    "label": cf["label"],
                    "fieldtype": cf["fieldtype"],
                    "options": cf.get("options", ""),
                    "insert_after": cf.get("insert_after"),
                    "module": "Custom",
                })
                self.report.custom_fields += 1
            except IngestionError as e:
                if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                    self.report.custom_fields += 1
                else:
                    self.report.errors.append(f"custom_field {cf['fieldname']}: {e}")

    # ---- masters -------------------------------------------------------------
    def _provision_uoms(self) -> None:
        for uom in {"tonnes", "Nm3", "litres", "kg", "kWh"}:
            try:
                self.client.insert("UOM", {"uom_name": uom, "must_be_whole_number": 0})
            except IngestionError as e:
                if "already exists" not in str(e).lower() and "duplicate" not in str(e).lower():
                    self.report.errors.append(f"uom {uom}: {e}")

    def _provision_item_groups(self) -> None:
        for group in {"raw_material", "fuel", "feedstock", "finished_good"}:
            try:
                self.client.insert("Item Group", {
                    "item_group_name": group,
                    "parent_item_group": "All Item Groups",
                    "is_group": 0,
                })
            except IngestionError as e:
                if "already exists" not in str(e).lower() and "duplicate" not in str(e).lower():
                    self.report.errors.append(f"item_group {group}: {e}")

    def _provision_items(self) -> None:
        for it in self.profile.items:
            payload = {
                "item_code": it.item_code,
                "item_name": it.item_name,
                "item_group": it.item_group,
                "stock_uom": it.uom,
                "is_stock_item": 0 if it.uom == "kWh" else 1,
                "include_item_in_manufacturing": 1 if not it.is_finished else 0,
                "custom_cn_code": it.cn_code,
                "custom_facility_code": self.profile.facility_code,
                "custom_sector": self.profile.sector,
                "custom_recycled_content_pct": it.recycled_content_pct,
            }
            try:
                self.client.upsert("Item", payload, name_field="item_code")
                self.report.items += 1
            except IngestionError as e:
                self.report.errors.append(f"item {it.item_code}: {e}")

    def _provision_suppliers(self) -> None:
        for s in self.profile.suppliers:
            try:
                self.client.upsert("Supplier", {
                    "supplier_name": s.supplier_name,
                    "supplier_group": s.supplier_group,
                    "country": _country_code_to_name(s.country),
                    "custom_country_code": s.country,
                }, name_field="supplier_name")
                self.report.suppliers += 1
            except IngestionError as e:
                self.report.errors.append(f"supplier {s.supplier_name}: {e}")

    def _provision_customers(self) -> None:
        for c in self.profile.eu_customers:
            try:
                self.client.upsert("Customer", {
                    "customer_name": c.supplier_name,
                    "customer_group": "Commercial",
                    "territory": "All Territories",
                    "customer_type": "Company",
                }, name_field="customer_name")
                self.report.customers += 1
            except IngestionError as e:
                self.report.errors.append(f"customer {c.supplier_name}: {e}")

    # ---- BOMs ----------------------------------------------------------------
    def _provision_boms(self) -> None:
        for product in self.profile.products:
            finished_item = self._lookup_item(product.item_code)
            payload = {
                "doctype": "BOM",
                "item": product.item_code,
                "quantity": 1,
                "is_active": 1,
                "is_default": 1,
                "with_operations": 0,
                "items": [
                    {
                        "item_code": ln.input_item,
                        "qty": ln.qty_per_tonne_output,
                        "uom": ln.uom,
                        "stock_uom": ln.uom,
                        "custom_facility_code": self.profile.facility_code,
                        "custom_product_cn_code": finished_item.cn_code if finished_item else "",
                        "custom_input_cn_code": self._cn_for(ln.input_item),
                        "custom_recycled_content_pct": ln.recycled_content_pct,
                    }
                    for ln in product.bom
                ],
            }
            try:
                self.client.insert("BOM", payload)
                self.report.boms += 1
            except IngestionError as e:
                # already exists for this item: fine
                if "already exists" not in str(e).lower() and "duplicate" not in str(e).lower():
                    self.report.errors.append(f"bom {product.item_code}: {e}")

    # ---- Cost centres (Block C2.2 sub-process allocation) -------------------
    def _provision_cost_centres(self) -> None:
        for cc in self.profile.cost_centres:
            try:
                self.client.insert("Cost Center", {
                    "cost_center_name": cc,
                    "parent_cost_center": f"{self.profile.legal_name} - {self.profile.legal_name[:3].upper()}",
                    "company": self.profile.legal_name,
                    "is_group": 0,
                })
                self.report.cost_centres += 1
            except IngestionError as e:
                if "already exists" not in str(e).lower() and "duplicate" not in str(e).lower():
                    # Cost-center insert is finicky in fresh installs — log and move on.
                    self.report.errors.append(f"cost_center {cc}: {e}")

    # ---- Stoichiometric driver: monthly demand plan ------------------------
    def _build_monthly_plans(self) -> list[dict]:
        """Returns one dict per month with planned output per product, applying
        seasonality, shutdowns, and a small random shock. POs are then sized
        from the BOM ratios so aggregate mass balance holds within ±5%."""
        today = date.today()
        first_month = (today.replace(day=1)
                       - timedelta(days=self.profile.months * 31)).replace(day=1)

        plans: list[dict] = []
        for offset in range(self.profile.months):
            month_start = _add_months(first_month, offset)
            seasonal = self.profile.seasonality[month_start.month - 1]
            shutdown_factor = self._shutdown_factor(month_start)
            outputs: dict[str, float] = {}
            for prod in self.profile.products:
                base = prod.monthly_output_tonnes_mean
                shock = self.rand.gauss(0, prod.monthly_output_tonnes_sigma / max(base, 1e-6))
                qty = max(0.0, base * seasonal * shutdown_factor * (1 + shock))
                outputs[prod.item_code] = qty
            plans.append({"month_start": month_start, "outputs": outputs,
                          "seasonal": seasonal, "shutdown_factor": shutdown_factor})
        return plans

    def _shutdown_factor(self, month_start: date) -> float:
        for sh_month, sh_days, severity in self.profile.shutdowns:
            if month_start.month == sh_month:
                # If the whole month is shut down at `severity`, scale linearly.
                from calendar import monthrange
                days_in_month = monthrange(month_start.year, month_start.month)[1]
                normal_days = max(0, days_in_month - sh_days)
                return (normal_days + sh_days * severity) / days_in_month
        return 1.0

    # ---- transactional: Work Orders + Rework + Quality + Stock --------------
    def _generate_work_orders(self, monthly_plans: list[dict]) -> None:
        for plan in monthly_plans:
            month_start = plan["month_start"]
            for product in self.profile.products:
                planned_total = plan["outputs"][product.item_code]
                if planned_total <= 0:
                    continue
                # split planned tonnage across N work orders for the month
                n_orders = max(1, int(self.profile.work_orders_per_month
                                       / max(len(self.profile.products), 1)))
                per_order = planned_total / n_orders
                for i in range(n_orders):
                    qty = max(50, self.rand.gauss(per_order, per_order * 0.10))
                    self._emit_work_order(
                        product, qty, month_start, plan["shutdown_factor"], parent_run_id=None,
                    )

    def _emit_work_order(
        self, product: FinishedProduct, qty: float, month_start: date,
        shutdown_factor: float, parent_run_id: str | None,
    ) -> None:
        # Plant idles harder during shutdowns: spread starts more thinly.
        start_day = self.rand.randint(0, 27)
        start_dt = datetime.combine(month_start + timedelta(days=start_day), datetime.min.time())
        end_dt = start_dt + timedelta(hours=self.rand.randint(8, 36))

        # Outcome roll: rework / scrap / completed
        r = self.rand.random()
        if r < self.profile.scrap_rate:
            outcome, produced_factor, status = "Scrap", 0.0, "Stopped"
        elif r < self.profile.scrap_rate + self.profile.rework_rate:
            outcome, produced_factor, status = "Rework", self.rand.uniform(0.30, 0.70), "Completed"
        else:
            outcome, produced_factor, status = "Completed", self.rand.uniform(0.96, 1.00), "Completed"

        eu_share = max(0.0, min(1.0, self.rand.gauss(product.eu_export_share_mean, 0.06)))
        cn = self._cn_for(product.item_code)
        cost_centre = self.rand.choice(self.profile.cost_centres or ("site_total",))
        payload = {
            "doctype": "Work Order",
            "production_item": product.item_code,
            "qty": round(qty, 3),
            "produced_qty": round(qty * produced_factor, 3),
            "planned_start_date": start_dt.isoformat(),
            "planned_end_date": end_dt.isoformat(),
            "actual_start_date": start_dt.isoformat(),
            "actual_end_date": end_dt.isoformat(),
            "status": status,
            "company": self.profile.legal_name,
            "custom_facility_code": self.profile.facility_code,
            "custom_sector": self.profile.sector,
            "custom_cn_code": cn,
            "custom_eu_export_share": round(eu_share, 4),
            "custom_scrap_rate_pct": round(self.rand.uniform(0.4, 2.6) +
                                            (3.0 if outcome == "Rework" else 0.0), 2),
        }
        try:
            doc = self.client.insert("Work Order", payload)
            self.report.work_orders += 1
            wo_name = doc.get("name", "")
        except IngestionError as e:
            self.report.errors.append(f"work_order: {e}")
            return

        # Quality inspection always emitted (some fail)
        try:
            self.client.insert("Quality Inspection", {
                "inspection_type": "In Process",
                "reference_type": "Work Order",
                "reference_name": wo_name,
                "item_code": product.item_code,
                "sample_size": 1,
                "status": "Accepted" if outcome == "Completed" else "Rejected",
                "inspected_by": "QA Inspector",
                "report_date": end_dt.date().isoformat(),
            })
            self.report.quality_inspections += 1
        except IngestionError:
            pass  # QA doctype can vary across versions — skip silently

        # Stock Entry — manufacture (goods movement on completion)
        if outcome != "Scrap":
            try:
                self.client.insert("Stock Entry", {
                    "stock_entry_type": "Manufacture",
                    "work_order": wo_name,
                    "company": self.profile.legal_name,
                    "posting_date": end_dt.date().isoformat(),
                    "items": [{
                        "item_code": product.item_code,
                        "qty": round(qty * produced_factor, 3),
                        "uom": product.bom[0].uom if product.bom else "tonnes",
                        "basic_rate": 100,
                        "is_finished_item": 1,
                    }],
                })
                self.report.stock_entries += 1
            except IngestionError:
                pass  # depends on warehouse setup; skip in pwd image

        # Rework recursion (only one level deep)
        if outcome == "Rework" and parent_run_id is None:
            rework_qty = qty * (1 - produced_factor)
            if rework_qty > 0:
                self._emit_work_order(
                    product, rework_qty, month_start, shutdown_factor,
                    parent_run_id=wo_name,
                )
                self.report.rework_orders += 1

    # ---- transactional: Purchase Orders + Invoices (stoichiometric) ---------
    def _generate_purchase_orders(self, monthly_plans: list[dict]) -> None:
        """For each month, compute required inputs from BOM × planned output,
        then emit POs that satisfy that demand. Adds ±5% noise per PO so the
        mass balance is realistic but auditable."""
        for plan in monthly_plans:
            month_start = plan["month_start"]
            required: dict[str, dict] = {}  # item_code → {qty, uom}
            for product in self.profile.products:
                planned_t = plan["outputs"][product.item_code]
                if planned_t <= 0:
                    continue
                for ln in product.bom:
                    required.setdefault(
                        ln.input_item, {"qty": 0.0, "uom": ln.uom},
                    )["qty"] += planned_t * ln.qty_per_tonne_output * self.rand.uniform(0.97, 1.03)

            # Spread each item's monthly demand across 1-3 POs to different suppliers
            for item_code, req in required.items():
                suppliers = [s for s in self.profile.suppliers if item_code in s.sells_items]
                if not suppliers:
                    continue
                n_pos = self.rand.randint(1, min(3, len(suppliers)))
                chunks = _split_qty(req["qty"], n_pos, self.rand)
                for chunk, supplier in zip(chunks, self.rand.sample(suppliers, n_pos)):
                    self._emit_po(item_code, chunk, req["uom"], supplier, month_start)

    def _emit_po(self, item_code: str, qty: float, uom: str,
                 supplier: SupplierSpec, month_start: date) -> None:
        item = self._lookup_item(item_code)
        if not item or qty <= 0:
            return
        # Price drift: log-normal walk anchored to typical rate
        base_rate = self._typical_rate(item)
        monthly_shock = self.rand.gauss(0, self.profile.price_drift_sigma)
        rate = max(0.01, base_rate * (1 + monthly_shock))
        po_day = self.rand.randint(0, 27)
        po_date = month_start + timedelta(days=po_day)
        schedule_date = po_date + timedelta(days=self.rand.randint(5, 25))

        try:
            po_doc = self.client.insert("Purchase Order", {
                "doctype": "Purchase Order",
                "supplier": supplier.supplier_name,
                "transaction_date": po_date.isoformat(),
                "schedule_date": schedule_date.isoformat(),
                "company": self.profile.legal_name,
                "currency": self.profile.currency,
                "conversion_rate": 1,
                "items": [{
                    "item_code": item_code,
                    "qty": round(qty, 3),
                    "rate": round(rate, 4),
                    "uom": uom,
                    "stock_uom": uom,
                    "schedule_date": schedule_date.isoformat(),
                    "custom_facility_code": self.profile.facility_code,
                    "custom_cn_code": item.cn_code,
                    "custom_supplier_name": supplier.supplier_name,
                    "custom_supplier_country": supplier.country,
                }],
            })
            self.report.purchase_orders += 1
            po_name = po_doc.get("name")
        except IngestionError as e:
            self.report.errors.append(f"purchase_order: {e}")
            return

        # Invoice a fraction
        if po_name and self.rand.random() < self.invoice_ratio:
            try:
                self.client.insert("Purchase Invoice", {
                    "doctype": "Purchase Invoice",
                    "supplier": supplier.supplier_name,
                    "posting_date": (schedule_date + timedelta(days=self.rand.randint(0, 10))).isoformat(),
                    "company": self.profile.legal_name,
                    "currency": self.profile.currency,
                    "conversion_rate": 1,
                    "custom_facility_code": self.profile.facility_code,
                    "custom_invoice_category": _category_for_item(item),
                    "custom_po_number": po_name,
                    "items": [{
                        "item_code": item_code,
                        "qty": round(qty, 3),
                        "rate": round(rate, 4),
                        "uom": uom,
                        "stock_uom": uom,
                        "purchase_order": po_name,
                    }],
                })
                self.report.purchase_invoices += 1
            except IngestionError:
                pass

    # ---- transactional: Sales Invoices for EU exports -----------------------
    def _generate_sales_invoices(self, monthly_plans: list[dict]) -> None:
        """One Sales Invoice per (EU customer × month × product) for the
        EU-bound share of the planned output."""
        for plan in monthly_plans:
            month_start = plan["month_start"]
            for product in self.profile.products:
                eu_t = plan["outputs"][product.item_code] * product.eu_export_share_mean
                if eu_t <= 0 or not self.profile.eu_customers:
                    continue
                n_customers = min(3, len(self.profile.eu_customers))
                shares = _split_qty(eu_t, n_customers, self.rand)
                for share, customer in zip(shares, self.rand.sample(list(self.profile.eu_customers), n_customers)):
                    inv_date = month_start + timedelta(days=self.rand.randint(5, 27))
                    rate = self._typical_rate(self._lookup_item(product.item_code)) * 1.2
                    try:
                        self.client.insert("Sales Invoice", {
                            "doctype": "Sales Invoice",
                            "customer": customer.supplier_name,
                            "posting_date": inv_date.isoformat(),
                            "company": self.profile.legal_name,
                            "currency": "EUR",
                            "conversion_rate": 1,
                            "custom_facility_code": self.profile.facility_code,
                            "custom_invoice_category": "logistics",
                            "items": [{
                                "item_code": product.item_code,
                                "qty": round(share, 3),
                                "rate": round(rate, 2),
                                "uom": "tonnes",
                            }],
                        })
                        self.report.sales_invoices += 1
                    except IngestionError:
                        pass

    # ---- helpers -------------------------------------------------------------
    def _lookup_item(self, item_code: str) -> ItemSpec | None:
        for it in self.profile.items:
            if it.item_code == item_code:
                return it
        return None

    def _cn_for(self, item_code: str) -> str:
        it = self._lookup_item(item_code)
        return it.cn_code if it else "00000000"

    def _typical_qty(self, item: ItemSpec) -> float:
        unit = item.uom
        if unit == "tonnes":
            return round(self.rand.uniform(80, 2_500), 2)
        if unit == "Nm3":
            return round(self.rand.uniform(20_000, 600_000), 0)
        if unit == "litres":
            return round(self.rand.uniform(5_000, 80_000), 0)
        if unit == "kg":
            return round(self.rand.uniform(200, 8_000), 1)
        return round(self.rand.uniform(100, 1000), 2)

    def _typical_rate(self, item: ItemSpec) -> float:
        unit = item.uom
        if unit == "tonnes":
            return round(self.rand.uniform(150, 1_400), 2)
        if unit == "Nm3":
            return round(self.rand.uniform(0.18, 0.45), 4)
        if unit == "litres":
            return round(self.rand.uniform(0.6, 1.4), 4)
        if unit == "kg":
            return round(self.rand.uniform(0.4, 4.0), 4)
        return round(self.rand.uniform(0.1, 5), 4)


# --------------------------------------------------------------------------
# small helpers — module level so tests can poke them
# --------------------------------------------------------------------------

def _split_qty(total: float, n: int, rand) -> list[float]:
    """Split `total` into n positive shares with Dirichlet-like noise."""
    if n <= 1:
        return [total]
    weights = [rand.uniform(0.5, 1.5) for _ in range(n)]
    s = sum(weights)
    return [total * w / s for w in weights]


def _add_months(d: date, months: int) -> date:
    y, m = d.year, d.month + months
    while m > 12:
        y, m = y + 1, m - 12
    while m < 1:
        y, m = y - 1, m + 12
    return date(y, m, 1)


_COUNTRY_NAMES = {
    "MZ": "Mozambique", "ZA": "South Africa", "MA": "Morocco", "EG": "Egypt",
    "BR": "Brazil", "AU": "Australia", "RU": "Russia", "QA": "Qatar",
    "IN": "India", "CN": "China", "IE": "Ireland", "NL": "Netherlands",
    "IT": "Italy", "DZ": "Algeria", "CH": "Switzerland", "US": "United States",
    "IL": "Israel", "BY": "Belarus", "NO": "Norway", "DE": "Germany",
    "FR": "France", "BE": "Belgium", "AT": "Austria", "ES": "Spain", "PL": "Poland",
}


def _country_code_to_name(iso2: str) -> str:
    return _COUNTRY_NAMES.get(iso2, iso2)


def _category_for_item(item: ItemSpec) -> str:
    if item.item_group == "fuel":
        if "diesel" in item.item_name.lower():
            return "diesel"
        if "gas" in item.item_name.lower():
            return "natural_gas"
        return "fuel"
    if item.item_group == "feedstock":
        return "natural_gas"
    return "raw_material"
