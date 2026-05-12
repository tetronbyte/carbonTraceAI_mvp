"""OCR engine — text extraction for PDFs (digital + scanned) and images.

Strategy:
1. PDFs → try `pdfplumber` text extraction first (fast, accurate for digital PDFs).
2. If text yield is too low (likely scanned PDF), fall back to per-page tesseract OCR.
3. Images → tesseract directly with a light OpenCV preprocess (grayscale + threshold).

Returns raw text + a coarse confidence score; downstream parsing is in `invoice_parser`.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pdfplumber
import pytesseract
from PIL import Image, ImageOps

try:
    import cv2  # type: ignore
    import numpy as np  # type: ignore
    _HAS_CV2 = True
except ImportError:
    _HAS_CV2 = False

from config.settings import settings
from src.core.exceptions import OcrError
from src.utils.logger import get_logger

log = get_logger(__name__)

if settings.tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

# A page that yields fewer characters than this is treated as scanned.
_TEXT_THRESHOLD_CHARS = 80


@dataclass
class OcrResult:
    file_path: str
    text: str
    page_count: int
    method: str  # "pdfplumber" | "tesseract" | "mixed"
    avg_confidence: Optional[float] = None


class OcrEngine:
    def extract(self, path: str | Path) -> OcrResult:
        p = Path(path)
        if not p.exists():
            raise OcrError(f"File not found: {p}", path=str(p))
        suffix = p.suffix.lower()
        if suffix == ".pdf":
            return self._extract_pdf(p)
        if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}:
            return self._extract_image(p)
        raise OcrError(f"Unsupported file type: {suffix}", path=str(p))

    # ---- PDFs ----
    def _extract_pdf(self, path: Path) -> OcrResult:
        log.info("OCR: PDF %s", path)
        text_parts: list[str] = []
        used_ocr = False
        confidences: list[float] = []
        page_count = 0
        try:
            with pdfplumber.open(path) as pdf:
                page_count = len(pdf.pages)
                for page in pdf.pages:
                    txt = (page.extract_text() or "").strip()
                    if len(txt) < _TEXT_THRESHOLD_CHARS:
                        used_ocr = True
                        img = page.to_image(resolution=200).original
                        ocr_text, conf = self._ocr_pil_image(img)
                        text_parts.append(ocr_text)
                        confidences.append(conf)
                    else:
                        text_parts.append(txt)
        except Exception as exc:  # noqa: BLE001
            raise OcrError(f"PDF read failed: {exc}", path=str(path)) from exc

        method = "tesseract" if used_ocr and len(confidences) == page_count else (
            "mixed" if used_ocr else "pdfplumber"
        )
        avg_conf = sum(confidences) / len(confidences) if confidences else None
        return OcrResult(
            file_path=str(path),
            text="\n".join(text_parts),
            page_count=page_count,
            method=method,
            avg_confidence=avg_conf,
        )

    # ---- images ----
    def _extract_image(self, path: Path) -> OcrResult:
        log.info("OCR: image %s", path)
        img = Image.open(path)
        text, conf = self._ocr_pil_image(img)
        return OcrResult(
            file_path=str(path),
            text=text,
            page_count=1,
            method="tesseract",
            avg_confidence=conf,
        )

    # ---- core OCR call ----
    def _ocr_pil_image(self, img: Image.Image) -> tuple[str, float]:
        prepared = self._preprocess(img)
        data = pytesseract.image_to_data(
            prepared, output_type=pytesseract.Output.DICT, lang="eng"
        )
        confs = [int(c) for c in data.get("conf", []) if str(c).lstrip("-").isdigit() and int(c) >= 0]
        text = pytesseract.image_to_string(prepared, lang="eng")
        avg = (sum(confs) / len(confs) / 100.0) if confs else 0.0
        return text, round(avg, 3)

    @staticmethod
    def _preprocess(img: Image.Image):
        """Grayscale + threshold. Uses OpenCV when available, otherwise PIL."""
        if _HAS_CV2:
            cv_img = cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2GRAY)
            _, cv_img = cv2.threshold(cv_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return cv_img
        gray = ImageOps.grayscale(img)
        # simple PIL-only binarisation
        return gray.point(lambda p: 255 if p > 160 else 0)
