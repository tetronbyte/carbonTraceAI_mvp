"""Abstract ingestor — every source (ERP, manual, OCR) implements it.

Contract:
    fetch()  → iterable of raw records (dicts)
    map()    → raw record → list of canonical Pydantic models
    run()    → orchestrates fetch + map + persist + audit, returns IngestionResult

Sources differ only in fetch/map; persistence and audit are shared.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Sequence

from pydantic import BaseModel

from .exceptions import IngestionError, ValidationError
from .models import IngestionEvent, SourceMethod


@dataclass
class IngestionResult:
    event: IngestionEvent
    records: list[BaseModel] = field(default_factory=list)
    errors: list[dict[str, Any]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.event.error_count == 0

    def summary(self) -> str:
        return (
            f"[{self.event.source}/{self.event.stream}] "
            f"in={self.event.record_count} ok={self.event.ok_count} err={self.event.error_count}"
        )


class BaseIngestor(ABC):
    """Template-method base — subclasses only override fetch/map.

    `repository` is duck-typed: must expose .save_many(records) and .save_event(event).
    """

    source: SourceMethod
    stream: str

    def __init__(self, repository: Any, *, raw_path: str | None = None) -> None:
        if not getattr(self, "source", None) or not getattr(self, "stream", None):
            raise IngestionError(
                "Ingestor must define class attrs `source` and `stream`",
                ingestor=type(self).__name__,
            )
        self.repository = repository
        self.raw_path = raw_path

    # ---- to be implemented per source ----
    @abstractmethod
    def fetch(self, **kwargs: Any) -> Iterable[dict[str, Any]]:
        """Yield raw records from the source."""

    @abstractmethod
    def map(self, raw: dict[str, Any]) -> Sequence[BaseModel]:
        """Convert one raw record into zero-or-more canonical models."""

    # ---- shared template method ----
    def run(self, **fetch_kwargs: Any) -> IngestionResult:
        event = IngestionEvent(
            source=self.source,
            stream=self.stream,
            raw_path=self.raw_path,
        )
        result = IngestionResult(event=event)

        for raw in self.fetch(**fetch_kwargs):
            event.record_count += 1
            try:
                models = list(self.map(raw))
            except (ValidationError, Exception) as exc:  # noqa: BLE001
                event.error_count += 1
                result.errors.append({"raw": raw, "error": str(exc)})
                continue

            try:
                self.repository.save_many(models)
                event.ok_count += 1
                result.records.extend(models)
            except Exception as exc:  # noqa: BLE001
                event.error_count += 1
                result.errors.append({"raw": raw, "error": f"persist: {exc}"})

        event.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
        self.repository.save_event(event)
        return result
