"""Field extraction over OCR'd invoice text.

MVP scope: utility & fuel invoices (electricity, natural gas, diesel) since these
are the highest-leverage CBAM inputs (Block C). Extends easily — add a new
`_PATTERNS` group + a category classifier line.

Extraction approach: keyword-anchored regex over normalised text. Keeps the
OCR module dependency-free of LLM/calls; downstream calc engine doesn't need
the parser to be perfect — `needs_manual_review=True` flags low-confidence
extractions for the review queue.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


_AMOUNT_RE = r"([\d.,]+)"
_DATE_PATTERNS = [
    r"\b(\d{4}-\d{2}-\d{2})\b",
    r"\b(\d{2}/\d{2}/\d{4})\b",
    r"\b(\d{2}-\d{2}-\d{4})\b",
    r"\b(\d{1,2}\s+[A-Za-z]+\s+\d{4})\b",
]

_INVOICE_NO_RE = re.compile(
    r"(?:invoice\s*(?:no\.?|number|#)|inv\s*no\.?|inv\s*#|reference)\s*[:#]?\s*([A-Z0-9\-/]{4,})",
    re.IGNORECASE,
)
_VENDOR_RE = re.compile(
    r"(?:vendor|supplier|from|sold\s+by|biller)\s*[:\-]\s*(.+)",
    re.IGNORECASE,
)
_TOTAL_RE = re.compile(
    r"(?:total\s+(?:amount\s+)?due|grand\s+total|amount\s+payable|total)\s*[:\-]?\s*([A-Z]{3})?\s*"
    + _AMOUNT_RE,
    re.IGNORECASE,
)

# category → (qty regex, unit)
_QUANTITY_PATTERNS: dict[str, tuple[re.Pattern[str], str]] = {
    "electricity": (
        re.compile(r"(?:total\s+consumption|consumption|usage|kwh\s+used)\s*[:\-]?\s*" + _AMOUNT_RE + r"\s*kwh", re.IGNORECASE),
        "kWh",
    ),
    "natural_gas": (
        re.compile(r"(?:gas\s+consumed|consumption|volume)\s*[:\-]?\s*" + _AMOUNT_RE + r"\s*(?:nm3|m3|sm3)", re.IGNORECASE),
        "Nm3",
    ),
    "diesel": (
        re.compile(r"(?:quantity|volume|litres?\s+supplied)\s*[:\-]?\s*" + _AMOUNT_RE + r"\s*(?:l|ltrs?|litres)", re.IGNORECASE),
        "litres",
    ),
}

_CATEGORY_KEYWORDS = {
    "electricity": ["kwh", "electricity", "eskom", "edm", "onee", "egyptian electricity", "tanesco"],
    "natural_gas": ["natural gas", "nm3", "sm3", "gas supply", "lng", "methane"],
    "diesel": ["diesel", "gasoil", "fuel oil", "automotive gas oil"],
}

_CURRENCIES = {"USD", "EUR", "ZAR", "MZN", "MAD", "EGP", "GBP", "JPY"}


@dataclass
class ExtractedInvoice:
    vendor_name: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    category: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    confidence: float = 0.0
    needs_manual_review: bool = False


class InvoiceParser:
    """Extracts CBAM-relevant fields from OCR'd invoice text."""

    def parse(self, text: str, ocr_confidence: float | None = None) -> ExtractedInvoice:
        norm = self._normalise(text)
        category = self._classify(norm)
        quantity, unit = (None, None)
        if category and category in _QUANTITY_PATTERNS:
            quantity, unit = self._match_quantity(norm, category)

        ext = ExtractedInvoice(
            vendor_name=self._first_line_vendor(text) or self._match(_VENDOR_RE, norm),
            invoice_number=self._match(_INVOICE_NO_RE, norm),
            invoice_date=self._parse_date(self._match_any_date(norm)),
            category=category,
            quantity=quantity,
            unit=unit,
            total_amount=self._match_total(norm),
            currency=self._detect_currency(norm),
        )

        # combine OCR confidence with extraction completeness
        score = self._score_completeness(ext)
        ext.confidence = round(((ocr_confidence or 0.6) * 0.5) + (score * 0.5), 3)
        ext.needs_manual_review = ext.confidence < 0.6 or ext.total_amount is None
        return ext

    # ---- helpers ----
    @staticmethod
    def _normalise(text: str) -> str:
        return re.sub(r"[ \t]+", " ", text)

    @staticmethod
    def _classify(text: str) -> Optional[str]:
        lower = text.lower()
        for cat, kws in _CATEGORY_KEYWORDS.items():
            if any(k in lower for k in kws):
                return cat
        return None

    @staticmethod
    def _match(pattern: re.Pattern[str], text: str) -> Optional[str]:
        m = pattern.search(text)
        return m.group(1).strip() if m else None

    @staticmethod
    def _match_any_date(text: str) -> Optional[str]:
        for pat in _DATE_PATTERNS:
            m = re.search(pat, text)
            if m:
                return m.group(1)
        return None

    @staticmethod
    def _parse_date(s: str | None) -> Optional[date]:
        if not s:
            return None
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %B %Y", "%d %b %Y"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        return None

    @staticmethod
    def _match_quantity(text: str, category: str) -> tuple[Optional[float], Optional[str]]:
        pat, unit = _QUANTITY_PATTERNS[category]
        m = pat.search(text)
        if not m:
            return None, unit
        return _to_float(m.group(1)), unit

    @staticmethod
    def _match_total(text: str) -> Optional[float]:
        m = _TOTAL_RE.search(text)
        if not m:
            return None
        return _to_float(m.group(2))

    @staticmethod
    def _detect_currency(text: str) -> Optional[str]:
        upper = text.upper()
        for cur in _CURRENCIES:
            if cur in upper.split():
                return cur
        if "R " in upper or "ZAR" in upper:
            return "ZAR"
        if "EUR" in upper or "€" in text:
            return "EUR"
        return None

    @staticmethod
    def _first_line_vendor(text: str) -> Optional[str]:
        for line in text.splitlines():
            line = line.strip()
            if 3 < len(line) < 80 and re.search(r"[A-Za-z]", line):
                return line
        return None

    @staticmethod
    def _score_completeness(ext: ExtractedInvoice) -> float:
        fields = [
            ext.vendor_name, ext.invoice_number, ext.invoice_date,
            ext.category, ext.quantity, ext.total_amount,
        ]
        return sum(1 for f in fields if f is not None) / len(fields)


def _to_float(s: str) -> Optional[float]:
    try:
        cleaned = s.replace(",", "").replace(" ", "")
        return float(cleaned)
    except (ValueError, AttributeError):
        return None
