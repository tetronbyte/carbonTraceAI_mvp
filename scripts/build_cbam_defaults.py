"""Extract the official CBAM default values (Annex I of Implementing Regulation
(EU) 2025/2621 as replaced by IR 2026/1740) from the EUR-Lex HTML into
data/cbam_default_values_2026_1740.csv.

Usage: python scripts/build_cbam_defaults.py <path to IR_2026-1740 ... .html>
Source HTML: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601740
Local copy:  carbonTraceAI_general/CBAM/03_Default_Values_and_Benchmarks/IR_2026-1740_Correcting_default_values_Annex_I_and_IV.html
Run 2026-11-20: 12540 rows, 122 countries. Fallback table is titled "Other Countries and Territories".
"""
from __future__ import annotations

import csv
import html
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "cbam_default_values_2026_1740.csv"


def _cells(tr: str) -> list[str]:
    cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
    return [html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c))).strip() for c in cells]


def _num(s: str) -> str:
    s = s.replace(",", ".").strip()
    return s if re.fullmatch(r"\d+(\.\d+)?", s) else ""  # "-" / "see below" -> empty


def parse(src: str) -> list[dict]:
    annex = src[src.index(">Default values for goods imported"):]
    annex = annex[: annex.index("ANNEX IV")] if "ANNEX IV" in annex else annex
    rows: list[dict] = []
    for table in re.findall(r"<table.*?</table>", annex, re.S):
        trs = re.findall(r"<tr.*?</tr>", table, re.S)
        if len(trs) < 3 or "Product CN Code" not in trs[1]:
            continue
        country = _cells(trs[0])[0]
        sector = ""
        for tr in trs[2:]:
            c = _cells(tr)
            if len(c) != 6:
                continue
            if c[0] and not any(c[1:]):
                sector = c[0]
                continue
            code = re.sub(r"\D", "", c[0])
            if not code:
                continue
            rows.append({
                "country": country, "sector": sector, "cn_code": code, "description": c[1],
                "direct": _num(c[2]), "indirect": _num(c[3]), "total": _num(c[4]),
                "route": c[5].strip("()"),
            })
    return rows


if __name__ == "__main__":
    rows = parse(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert rows and any(r["country"].lower() == "other countries and territories" for r in rows), "parse failed"
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows, {len({r['country'] for r in rows})} countries -> {OUT}")
