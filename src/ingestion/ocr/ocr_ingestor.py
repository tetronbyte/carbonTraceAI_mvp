"""OCR ingestor — turns a folder of invoice PDFs/images into:
  1. an `InvoiceDocument` row (full audit, raw OCR text + confidence)
  2. when applicable, an `EnergyConsumption` row mapped from the parsed fields
     (so utility/fuel bills feed Block C straight away)
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Sequence

from pydantic import BaseModel

from src.core.base import BaseIngestor
from src.core.enums import (
    FuelType,
    MeterType,
    SourceMethod,
    UnitOfMeasure,
)
from src.core.models import EnergyConsumption, InvoiceDocument
from src.utils.logger import get_logger
from src.utils.raw_landing import RawLandingZone

from .invoice_parser import ExtractedInvoice, InvoiceParser
from .ocr_engine import OcrEngine

log = get_logger(__name__)

_CATEGORY_TO_METER: dict[str, tuple[MeterType, UnitOfMeasure, FuelType | None]] = {
    "electricity": (MeterType.ELECTRICITY_GRID, UnitOfMeasure.KWH, None),
    "natural_gas": (MeterType.NATURAL_GAS, UnitOfMeasure.NM3, FuelType.NATURAL_GAS),
    "diesel":      (MeterType.DIESEL_GENERATOR, UnitOfMeasure.LITRES, FuelType.DIESEL),
}


class OcrIngestor(BaseIngestor):
    source = SourceMethod.INVOICE
    stream = "ocr_invoices"

    def __init__(
        self,
        repository: Any,
        *,
        documents: Iterable[str | Path],
        facility_id: str,
        engine: OcrEngine | None = None,
        parser: InvoiceParser | None = None,
    ) -> None:
        self._documents = [Path(d) for d in documents]
        self.facility_id = facility_id
        self.engine = engine or OcrEngine()
        self.parser = parser or InvoiceParser()
        self._landing = RawLandingZone(source=self.source.value, stream=self.stream)
        super().__init__(repository, raw_path=str(self._landing.path))

    def fetch(self, **_: Any) -> Iterable[dict[str, Any]]:
        with self._landing.open() as writer:
            for doc_path in self._documents:
                if not doc_path.exists():
                    log.warning("Invoice missing: %s", doc_path)
                    continue
                ocr = self.engine.extract(doc_path)
                extracted: ExtractedInvoice = self.parser.parse(ocr.text, ocr.avg_confidence)
                payload: dict[str, Any] = {
                    "file_path": str(doc_path),
                    "ocr_method": ocr.method,
                    "ocr_confidence": ocr.avg_confidence,
                    "extracted": extracted.__dict__,
                    "raw_text": ocr.text[:5000],  # cap for landing
                }
                ref = writer.write(payload)
                payload["_raw_ref"] = ref
                yield payload

    def map(self, raw: dict[str, Any]) -> Sequence[BaseModel]:
        ext = raw["extracted"]
        ref = raw.get("_raw_ref")
        out: list[BaseModel] = [
            InvoiceDocument(
                source=SourceMethod.INVOICE,
                raw_ref=ref,
                file_path=raw["file_path"],
                vendor_name=ext.get("vendor_name"),
                invoice_number=ext.get("invoice_number"),
                invoice_date=_to_date(ext.get("invoice_date")),
                category=ext.get("category"),
                quantity=ext.get("quantity"),
                unit=ext.get("unit"),
                total_amount=ext.get("total_amount"),
                currency=ext.get("currency"),
                raw_text=raw.get("raw_text"),
                ocr_confidence=ext.get("confidence"),
                needs_manual_review=ext.get("needs_manual_review", True),
            )
        ]

        # If parsed enough to feed Block C, also emit an EnergyConsumption row.
        cat = ext.get("category")
        qty = ext.get("quantity")
        inv_date = _to_date(ext.get("invoice_date"))
        if cat in _CATEGORY_TO_METER and qty and inv_date:
            meter_type, unit, fuel = _CATEGORY_TO_METER[cat]
            out.append(
                EnergyConsumption(
                    source=SourceMethod.INVOICE,
                    raw_ref=ref,
                    facility_id=self.facility_id,
                    period_start=inv_date,
                    period_end=inv_date,
                    meter_type=meter_type,
                    quantity=float(qty),
                    unit=unit,
                    fuel_type=fuel,
                    supplier_name=ext.get("vendor_name"),
                    quality_flag="estimated" if ext.get("needs_manual_review") else "ok",
                )
            )
        return out


def _to_date(v: Any) -> date | None:
    if v is None or isinstance(v, date):
        return v
    try:
        return date.fromisoformat(str(v))
    except ValueError:
        return None
