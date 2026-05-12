"""OCR demo — runs the OCR ingestor against one or more invoice paths.

Usage:
    python -m scripts.ocr_invoice_demo data/samples/sample_fuel_invoice.pdf

If no path is given, generates a synthetic text invoice (PNG) so the demo
runs end-to-end without external assets.
"""
from __future__ import annotations

import sys
from pathlib import Path

from src.ingestion.orchestrator import IngestionOrchestrator


def _make_sample_invoice(path: Path) -> Path:
    """Write a synthetic, text-only invoice PNG so OCR has something to chew."""
    from PIL import Image, ImageDraw, ImageFont

    text = (
        "Eskom Holdings SOC Ltd\n"
        "VAT: 4740101508\n\n"
        "Invoice Number: INV-2026-00821\n"
        "Invoice Date: 2026-04-30\n"
        "Customer: Hillside Aluminium\n\n"
        "Description: Electricity supply, April 2026\n"
        "Total consumption: 712,450,000 kWh\n"
        "Tariff: Megaflex\n\n"
        "Total amount due: ZAR 1,245,876,500\n"
    )
    img = Image.new("RGB", (1000, 600), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    draw.multiline_text((40, 40), text, fill="black", font=font, spacing=8)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    return path


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        docs = [Path(a) for a in argv[1:]]
    else:
        sample = Path("data/samples/sample_electricity_invoice.png")
        if not sample.exists():
            _make_sample_invoice(sample)
        docs = [sample]

    orch = IngestionOrchestrator()
    orch.run_ocr(docs, facility_id="HILLSIDE-ZA-01")
    print(orch.report.summary())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
