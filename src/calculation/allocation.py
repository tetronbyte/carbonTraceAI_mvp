"""Coproduct allocation per CBAM IR Annex IV §A.5.

Three permitted bases:
  - MASS:    weight share of each product
  - ENERGY:  energy content (NCV) share
  - ECONOMIC: market-value share

Falls through to NONE when there's only one product on the run.
"""
from __future__ import annotations

from src.core.enums import AllocationMethod


def allocate(
    total_emissions_tco2e: float,
    weights: dict[str, float],
    method: AllocationMethod = AllocationMethod.MASS,
) -> dict[str, float]:
    """Split `total_emissions` across keys of `weights` proportionally."""
    if method == AllocationMethod.NONE or not weights:
        return {next(iter(weights), "main"): total_emissions_tco2e} if weights else {}
    total_w = sum(w for w in weights.values() if w > 0)
    if total_w <= 0:
        # equal split fallback
        n = len(weights)
        return {k: total_emissions_tco2e / n for k in weights}
    return {k: total_emissions_tco2e * (w / total_w) for k, w in weights.items()}


def allocation_share(weights: dict[str, float], product: str) -> float:
    total = sum(w for w in weights.values() if w > 0)
    if total <= 0 or product not in weights:
        return 1.0
    return weights[product] / total
