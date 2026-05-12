"""Domain exceptions — kept thin; carry code + context for upstream UIs."""
from __future__ import annotations

from typing import Any


class CarbonTraceError(Exception):
    """Root for all carbonTraceAI errors."""

    code: str = "carbontrace_error"

    def __init__(self, message: str, **context: Any) -> None:
        super().__init__(message)
        self.message = message
        self.context = context

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, "context": self.context}


class ValidationError(CarbonTraceError):
    code = "validation_error"


class IngestionError(CarbonTraceError):
    code = "ingestion_error"


class SchemaError(CarbonTraceError):
    code = "schema_error"


class OcrError(CarbonTraceError):
    code = "ocr_error"
