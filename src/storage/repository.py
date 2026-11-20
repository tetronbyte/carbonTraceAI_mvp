"""SQLite-backed canonical store.

One table per canonical model + a generic `ingestion_events` audit table.
Tables hold JSON-encoded payloads alongside indexed columns — keeps the schema
narrow while preserving full Pydantic fidelity for the calc engine.

Migration path: swap engine URL to Postgres, columns stay the same.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from typing import Iterable, Type

from pydantic import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    delete,
    func,
    insert,
    select,
)
from sqlalchemy.engine import Engine

from config.settings import settings
from src.core.models import (
    AluminiumProcessRecord,
    CarbonPricePaid,
    CHPRecord,
    CostCentreAllocation,
    EnergyConsumption,
    Facility,
    FertiliserProcessRecord,
    FugitiveEmission,
    GLEntry,
    IngestionEvent,
    InvoiceDocument,
    MRPlan,
    MonitoringMeta,
    OutboundShipment,
    PrecursorPurchase,
    ProcessBoundary,
    ProductionRun,
    QualityInspection,
    RECsCertificate,
    StockMovement,
)
from src.utils.logger import get_logger

log = get_logger(__name__)


_MODEL_TABLE_MAP: dict[Type[BaseModel], str] = {
    Facility: "facilities",
    ProductionRun: "production_runs",
    EnergyConsumption: "energy_consumption",
    AluminiumProcessRecord: "aluminium_process",
    FertiliserProcessRecord: "fertiliser_process",
    PrecursorPurchase: "precursor_purchases",
    FugitiveEmission: "fugitive_emissions",
    OutboundShipment: "outbound_shipments",
    MonitoringMeta: "monitoring_meta",
    InvoiceDocument: "invoice_documents",
    # New CBAM-completeness tables
    ProcessBoundary: "process_boundary",
    RECsCertificate: "recs_certificates",
    CHPRecord: "chp_records",
    CarbonPricePaid: "carbon_price_paid",
    MRPlan: "mr_plans",
    CostCentreAllocation: "cost_centre_allocation",
    StockMovement: "stock_movements",
    GLEntry: "gl_entries",
    QualityInspection: "quality_inspections",
}


def _json_default(obj: object) -> str:
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"unserialisable: {type(obj)}")


class Repository:
    """Thin persistence layer. One file per process is fine for the MVP."""

    def __init__(self, db_url: str | None = None) -> None:
        self.engine: Engine = create_engine(db_url or settings.db_url, future=True)
        self.metadata = MetaData()
        self._tables: dict[str, Table] = {}
        self._define_tables()
        self.metadata.create_all(self.engine)

    # ---- schema ----
    def _define_tables(self) -> None:
        common = lambda name: Table(  # noqa: E731
            name,
            self.metadata,
            Column("id", String, primary_key=True),
            Column("source", String, index=True),
            Column("ingested_at", DateTime, index=True),
            Column("facility_id", String, index=True, nullable=True),
            Column("period_start", String, index=True, nullable=True),
            Column("period_end", String, index=True, nullable=True),
            Column("payload", Text, nullable=False),
            Column("raw_ref", String, nullable=True),
        )
        for model, name in _MODEL_TABLE_MAP.items():
            self._tables[name] = common(name)

        self._tables["ingestion_events"] = Table(
            "ingestion_events",
            self.metadata,
            Column("id", String, primary_key=True),
            Column("source", String, index=True),
            Column("stream", String, index=True),
            Column("record_count", Integer),
            Column("ok_count", Integer),
            Column("error_count", Integer),
            Column("started_at", DateTime),
            Column("finished_at", DateTime),
            Column("raw_path", String),
            Column("notes", Text, nullable=True),
        )

    # ---- writes ----
    def save_many(self, records: Iterable[BaseModel]) -> int:
        rows_by_table: dict[str, list[dict]] = {}
        n = 0
        for rec in records:
            table_name = _MODEL_TABLE_MAP.get(type(rec))
            if not table_name:
                raise ValueError(f"No table mapping for model {type(rec).__name__}")
            payload = rec.model_dump(mode="json")
            row = {
                "id": payload.get("id"),
                "source": payload.get("source"),
                "ingested_at": _coerce_dt(payload.get("ingested_at")),
                "facility_id": payload.get("facility_id"),
                "period_start": _coerce_str(payload.get("period_start") or payload.get("reporting_period_start")),
                "period_end": _coerce_str(payload.get("period_end") or payload.get("reporting_period_end")),
                "payload": json.dumps(payload, default=_json_default),
                "raw_ref": payload.get("raw_ref"),
            }
            rows_by_table.setdefault(table_name, []).append(row)
            n += 1

        with self.engine.begin() as conn:
            for table_name, rows in rows_by_table.items():
                conn.execute(insert(self._tables[table_name]), rows)
        return n

    def save_event(self, event: IngestionEvent) -> None:
        row = event.model_dump(mode="json")
        row["started_at"] = _coerce_dt(row["started_at"])
        row["finished_at"] = _coerce_dt(row.get("finished_at"))
        with self.engine.begin() as conn:
            conn.execute(insert(self._tables["ingestion_events"]), [row])

    def clear_facility(self, facility_id: str, legal_entity_name: str | None = None) -> int:
        """Delete one facility's canonical rows so a re-pull replaces them.

        Rows get a fresh UUID on every ingest, so without this each pipeline run
        adds to the previous one and double-counts output and emissions.
        `ingestion_events` is an append-only audit log and is left alone.
        Facility rows carry no facility_id, so they match on legal entity name.
        UNASSIGNED rows (e.g. GL entries, which have no facility) are re-pulled
        too, so they are cleared as well.
        """
        removed = 0
        with self.engine.begin() as conn:
            for name, table in self._tables.items():
                if name in ("ingestion_events", "facilities"):
                    continue
                removed += conn.execute(
                    delete(table).where(table.c.facility_id.in_((facility_id, "UNASSIGNED")))
                ).rowcount
            if legal_entity_name:
                facilities = self._tables["facilities"]
                for row in conn.execute(select(facilities)).mappings().all():
                    if json.loads(row["payload"]).get("legal_entity_name") == legal_entity_name:
                        removed += conn.execute(
                            delete(facilities).where(facilities.c.id == row["id"])
                        ).rowcount
        return removed

    # ---- reads (for downstream layers) ----
    def count(self, table: str) -> int:
        with self.engine.connect() as conn:
            t = self._tables[table]
            return int(conn.execute(select(func.count()).select_from(t)).scalar_one())

    def fetch_all(self, table: str) -> list[dict]:
        with self.engine.connect() as conn:
            t = self._tables[table]
            rows = conn.execute(select(t)).mappings().all()
            return [dict(r) for r in rows]

    def fetch_payloads(self, table: str) -> list[dict]:
        return [json.loads(r["payload"]) for r in self.fetch_all(table)]


def _coerce_dt(v):
    if v is None or isinstance(v, datetime):
        return v
    if isinstance(v, str):
        try:
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def _coerce_str(v):
    if v is None:
        return None
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    return str(v)
