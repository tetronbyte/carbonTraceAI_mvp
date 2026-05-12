"""IngestionOrchestrator — single entry point that runs the four MVP sources
(ERPNext, manual, supplier portal, OCR) and returns a consolidated report.

Downstream layers (cleaning, calc) read from the same `Repository` regardless
of which sources actually ran.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from src.core.base import IngestionResult
from src.ingestion.erp.erp_ingestor import ErpIngestor
from src.ingestion.erp.erpnext_client import ERPNextClient, ERPNextCredentials
from src.ingestion.erp.erpnext_runner import ERPNextRunner
from src.ingestion.manual.manual_ingestor import (
    ManualIngestor,
    SensorIngestor,
    SupplierPortalIngestor,
)
from src.ingestion.ocr.ocr_ingestor import OcrIngestor
from src.storage.repository import Repository
from src.utils.logger import get_logger

log = get_logger(__name__)


@dataclass
class PipelineReport:
    results: list[IngestionResult] = field(default_factory=list)

    def add(self, r: IngestionResult) -> None:
        self.results.append(r)

    def summary(self) -> str:
        lines = [r.summary() for r in self.results]
        total_in = sum(r.event.record_count for r in self.results)
        total_ok = sum(r.event.ok_count for r in self.results)
        total_err = sum(r.event.error_count for r in self.results)
        lines.append(f"TOTAL  in={total_in} ok={total_ok} err={total_err}")
        return "\n".join(lines)


class IngestionOrchestrator:
    """Composable orchestrator. Pass only the sources you want to run."""

    def __init__(self, repository: Repository | None = None) -> None:
        self.repository = repository or Repository()
        self.report = PipelineReport()

    # ---- ERPNext (direct REST) ----
    def run_erpnext_direct(self, creds: ERPNextCredentials) -> PipelineReport:
        """Pull every CBAM-relevant stream from a live ERPNext instance and
        ingest it into the canonical store."""
        log.info("Running ERPNext direct REST sync against %s", creds.base_url)
        client = ERPNextClient(creds)
        if not client.ping():
            raise ConnectionError(f"ERPNext unreachable at {creds.base_url}")
        runner = ERPNextRunner(client)
        landings = runner.sync_all()
        for stream, path in landings.items():
            ing = ErpIngestor(self.repository, stream=stream, landing_path=path)
            self.report.add(ing.run())
        return self.report

    def run_erp_from_landings(self, stream_to_path: dict[str, Path]) -> PipelineReport:
        """Consume an existing JSONL landing — used after an Airbyte sync."""
        for stream, path in stream_to_path.items():
            ing = ErpIngestor(self.repository, stream=stream, landing_path=path)
            self.report.add(ing.run())
        return self.report

    # ---- Manual / Sensor (manual) / Supplier ----
    def run_manual(self, form_id: str, submissions: Iterable[dict[str, Any]]) -> PipelineReport:
        ingestor = ManualIngestor(self.repository, form_id=form_id, submissions=submissions)
        self.report.add(ingestor.run())
        return self.report

    def run_sensor(self, submissions: Iterable[dict[str, Any]]) -> PipelineReport:
        """No SCADA in the MVP — meter readings are entered manually via the
        same form contract. Tagged source=METER for downstream calc parity."""
        ingestor = SensorIngestor(self.repository, submissions=submissions)
        self.report.add(ingestor.run())
        return self.report

    def run_supplier(self, submissions: Iterable[dict[str, Any]]) -> PipelineReport:
        ingestor = SupplierPortalIngestor(self.repository, submissions=submissions)
        self.report.add(ingestor.run())
        return self.report

    # ---- OCR ----
    def run_ocr(self, documents: Iterable[str | Path], facility_id: str) -> PipelineReport:
        ingestor = OcrIngestor(self.repository, documents=documents, facility_id=facility_id)
        self.report.add(ingestor.run())
        return self.report
