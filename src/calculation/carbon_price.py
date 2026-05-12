"""Block G — carbon price paid in country of origin, converted to EUR.

CBAM IR 2023/1773 Annex IV §3 permits a deduction equal to the per-tonne
carbon price actually paid in the origin country, capped at the EUA spot
price for the relevant quarter.
"""
from __future__ import annotations

from . import lookup_tables as lut


def carbon_price_paid_eur_per_tco2e(payloads: list[dict]) -> float:
    """Weighted-average carbon price actually paid across all CarbonPricePaid
    rows in a period. Returns EUR per tCO2e."""
    if not payloads:
        return 0.0
    total_eur = 0.0
    total_tco2e = 0.0
    for p in payloads:
        net = p.get("net_taxable_tco2e") or 0
        if net <= 0:
            continue
        eur = p.get("total_paid_eur")
        if not eur and p.get("total_paid_local") and p.get("local_currency"):
            eur = float(p["total_paid_local"]) * lut.fx_to_eur(p["local_currency"])
        total_eur += float(eur or 0)
        total_tco2e += float(net)
    if total_tco2e <= 0:
        return 0.0
    return total_eur / total_tco2e
