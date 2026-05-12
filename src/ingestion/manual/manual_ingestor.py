"""Manual entry ingestor — accepts validated form payloads.

Three flavours, all sharing the same plumbing:
- ManualIngestor          — generic forms (facility, fugitive, monitoring, process)
- SensorIngestor          — manual sensor/meter readings (until SCADA online)
- SupplierPortalIngestor  — Block E supplier declarations

Each persists raw submission JSONL to the landing zone and writes the
canonical Pydantic model into the repository.
"""
from __future__ import annotations

from typing import Any, Iterable, Sequence

from pydantic import BaseModel, ValidationError as PydanticValidationError

from src.core.base import BaseIngestor
from src.core.enums import SourceMethod
from src.core.exceptions import ValidationError
from src.core.models import (
    AluminiumProcessRecord,
    CarbonPricePaid,
    CHPRecord,
    CostCentreAllocation,
    EnergyConsumption,
    Facility,
    FertiliserProcessRecord,
    FugitiveEmission,
    InvoiceDocument,
    MRPlan,
    MonitoringMeta,
    OutboundShipment,
    PrecursorPurchase,
    ProcessBoundary,
    ProductionRun,
    RECsCertificate,
)
from src.utils.logger import get_logger
from src.utils.raw_landing import RawLandingZone

from .form_definitions import get_form

log = get_logger(__name__)


# Form id → canonical Pydantic model
_FORM_MODEL_MAP: dict[str, type[BaseModel]] = {
    "facility": Facility,
    "aluminium_process_monthly": AluminiumProcessRecord,
    "fertiliser_process_monthly": FertiliserProcessRecord,
    "sensor_reading_manual": EnergyConsumption,
    "supplier_portal_submission": PrecursorPurchase,
    "fugitive_annual": FugitiveEmission,
    "monitoring_meta": MonitoringMeta,
    "process_boundary": ProcessBoundary,
    "recs_certificate": RECsCertificate,
    "chp_record": CHPRecord,
    "carbon_price_paid": CarbonPricePaid,
    "mr_plan": MRPlan,
    "cost_centre_allocation": CostCentreAllocation,
}


class _BaseManualIngestor(BaseIngestor):
    source = SourceMethod.MANUAL

    def __init__(
        self,
        repository: Any,
        *,
        form_id: str,
        submissions: Iterable[dict[str, Any]] | None = None,
    ) -> None:
        self.form_id = form_id
        self.stream = form_id
        self.form = get_form(form_id)
        self._submissions = list(submissions or [])
        self._landing = RawLandingZone(source=self.source.value, stream=form_id)
        super().__init__(repository, raw_path=str(self._landing.path))

    def add(self, submission: dict[str, Any]) -> None:
        """Queue a submission for the next run()."""
        self._submissions.append(submission)

    def fetch(self, **_: Any) -> Iterable[dict[str, Any]]:
        with self._landing.open() as writer:
            for sub in self._submissions:
                ref = writer.write(sub)
                row = dict(sub)
                row["_raw_ref"] = ref
                yield row

    def map(self, raw: dict[str, Any]) -> Sequence[BaseModel]:
        model_cls = _FORM_MODEL_MAP.get(self.form_id)
        if not model_cls:
            return []
        self._validate_against_form(raw)
        payload = {k: v for k, v in raw.items() if not k.startswith("_")}
        payload.setdefault("source", self.source.value)
        payload["raw_ref"] = raw.get("_raw_ref")
        try:
            return [model_cls(**payload)]
        except PydanticValidationError as e:
            raise ValidationError(
                f"Form {self.form_id!r} payload failed model validation",
                errors=e.errors(),
            ) from e

    def _validate_against_form(self, raw: dict[str, Any]) -> None:
        missing = [
            f["name"]
            for f in self.form["fields"]
            if f.get("required") and raw.get(f["name"]) in (None, "", [])
        ]
        if missing:
            raise ValidationError(
                f"Form {self.form_id!r} missing required fields: {missing}",
                missing=missing,
            )


class ManualIngestor(_BaseManualIngestor):
    """Generic manual form ingestor. Stream/source = MANUAL."""


class SensorIngestor(_BaseManualIngestor):
    """Manual sensor/meter readings until a live SCADA pull is wired up."""

    source = SourceMethod.METER  # tag readings as metered for downstream calcs

    def __init__(
        self,
        repository: Any,
        submissions: Iterable[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(repository, form_id="sensor_reading_manual", submissions=submissions)


class SupplierPortalIngestor(_BaseManualIngestor):
    """Block E supplier portal submissions — flagged as SUPPLIER source."""

    source = SourceMethod.SUPPLIER

    def __init__(
        self,
        repository: Any,
        submissions: Iterable[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(repository, form_id="supplier_portal_submission", submissions=submissions)
