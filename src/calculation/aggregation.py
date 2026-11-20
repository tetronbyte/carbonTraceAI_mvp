"""Monthly → quarterly (and annual) aggregation of raw inputs.

The calc engine consumes monthly windows; the CBAM definitive-period report is
quarterly. This module handles both period derivation and the rollup of
activity totals across canonical tables.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Iterable


def quarter_of(d: date) -> str:
    return f"{d.year}-Q{((d.month - 1) // 3) + 1}"


def quarter_bounds(quarter: str) -> tuple[date, date]:
    """e.g. '2026-Q2' → (date(2026,4,1), date(2026,6,30))."""
    y, q = quarter.split("-Q")
    y = int(y); q = int(q)
    start_month = (q - 1) * 3 + 1
    end_month = start_month + 2
    from calendar import monthrange
    end_day = monthrange(y, end_month)[1]
    return date(y, start_month, 1), date(y, end_month, end_day)


def overlaps(period_start: date, period_end: date, q_start: date, q_end: date) -> bool:
    return not (period_end < q_start or period_start > q_end)


@dataclass
class AggregatedActivity:
    """Aggregated activity totals for one (facility, product CN, quarter)."""
    facility_id: str
    cn_code: str
    quarter: str
    production_runs: list[dict] = field(default_factory=list)
    fuel_consumption: list[dict] = field(default_factory=list)
    electricity_consumption: list[dict] = field(default_factory=list)
    steam_consumption: list[dict] = field(default_factory=list)
    precursors: list[dict] = field(default_factory=list)
    process_records_al: list[dict] = field(default_factory=list)
    process_records_fert: list[dict] = field(default_factory=list)
    fugitive: list[dict] = field(default_factory=list)
    recs: list[dict] = field(default_factory=list)
    carbon_price_paid: list[dict] = field(default_factory=list)

    @property
    def total_output_t(self) -> float:
        return sum(p.get("output_tonnes", 0) for p in self.production_runs)

    @property
    def eu_export_t(self) -> float:
        return sum(p.get("eu_export_tonnes", 0) for p in self.production_runs)


def aggregate_by_quarter(
    facility_id: str,
    quarter: str,
    production_payloads: Iterable[dict],
    energy_payloads: Iterable[dict],
    precursor_payloads: Iterable[dict],
    aluminium_payloads: Iterable[dict],
    fertiliser_payloads: Iterable[dict],
    fugitive_payloads: Iterable[dict],
    recs_payloads: Iterable[dict],
    carbon_price_payloads: Iterable[dict],
) -> dict[str, AggregatedActivity]:
    """Bucket every input by CN code for one facility + quarter."""
    q_start, q_end = quarter_bounds(quarter)
    buckets: dict[str, AggregatedActivity] = defaultdict(
        lambda: AggregatedActivity(facility_id=facility_id, cn_code="?", quarter=quarter)
    )

    # production — CN comes from each row
    for r in production_payloads:
        if r.get("facility_id") != facility_id:
            continue
        if not _row_in_q(r, "run_started_at", q_start, q_end):
            continue
        b = buckets[r["product_cn_code"]]
        b.cn_code = r["product_cn_code"]
        b.production_runs.append(r)

    # energy — no CN linkage, so attach the whole bucket to *every* CN seen
    cns = list(buckets.keys()) or ["?"]
    for e in energy_payloads:
        if e.get("facility_id") != facility_id:
            continue
        if not _row_in_q(e, "period_start", q_start, q_end):
            continue
        for cn in cns:
            b = buckets[cn]; b.cn_code = cn
            if e.get("meter_type", "").startswith("electricity"):
                b.electricity_consumption.append(e)
            elif e.get("meter_type") == "steam":
                b.steam_consumption.append(e)
            else:
                b.fuel_consumption.append(e)

    # precursors — bucket by *consuming* CN; for the MVP we attach by month
    # match to the largest production CN in that month (simple heuristic).
    precursor_rows = [
        p for p in precursor_payloads
        if p.get("facility_id") == facility_id and _row_in_q(p, "purchase_date", q_start, q_end)
    ]
    for p in _supplier_declarations_win(precursor_rows):
        primary_cn = _primary_cn(buckets) or "?"
        b = buckets[primary_cn]; b.cn_code = primary_cn
        b.precursors.append(p)

    for r in aluminium_payloads:
        if r.get("facility_id") != facility_id:
            continue
        if not _row_in_q(r, "period_start", q_start, q_end):
            continue
        for cn in (k for k in buckets if k.startswith("76")):
            buckets[cn].process_records_al.append(r)

    for r in fertiliser_payloads:
        if r.get("facility_id") != facility_id:
            continue
        if not _row_in_q(r, "period_start", q_start, q_end):
            continue
        for cn in (k for k in buckets if k.startswith(("28", "31"))):
            buckets[cn].process_records_fert.append(r)

    for f in fugitive_payloads:
        if f.get("facility_id") != facility_id:
            continue
        if not _row_in_q(f, "period_start", q_start, q_end):
            continue
        # fugitive emissions allocate across all CNs at the facility (mass basis)
        for cn in buckets:
            buckets[cn].fugitive.append(f)

    for r in recs_payloads:
        if r.get("facility_id") != facility_id:
            continue
        if not _row_in_q(r, "period_start", q_start, q_end):
            continue
        for cn in buckets:
            buckets[cn].recs.append(r)

    for c in carbon_price_payloads:
        if c.get("facility_id") != facility_id:
            continue
        if not _row_in_q(c, "period_start", q_start, q_end):
            continue
        for cn in buckets:
            buckets[cn].carbon_price_paid.append(c)

    return dict(buckets)


def _supplier_declarations_win(rows: list[dict]) -> list[dict]:
    """A supplier-portal row describes the same goods as the ERP PO it cites, so
    it replaces that PO row instead of adding its tonnage a second time."""
    declared_pos = {
        p["po_number"] for p in rows
        if p.get("source") == "SUPPLIER" and p.get("po_number")
    }
    return [
        p for p in rows
        if p.get("source") == "SUPPLIER" or p.get("po_number") not in declared_pos
    ]


def _row_in_q(row: dict, date_key: str, q_start: date, q_end: date) -> bool:
    v = row.get(date_key)
    if not v:
        return False
    if isinstance(v, str):
        try:
            d = date.fromisoformat(v[:10])
        except ValueError:
            return False
    elif isinstance(v, date):
        d = v
    else:
        return False
    return q_start <= d <= q_end


def _primary_cn(buckets: dict) -> str | None:
    if not buckets:
        return None
    return max(
        buckets, key=lambda cn: sum(p.get("output_tonnes", 0) for p in buckets[cn].production_runs)
    )
