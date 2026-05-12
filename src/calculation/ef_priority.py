"""Emission-factor priority resolution.

Per CBAM IR 2023/1773 §A.4 the preference order for any EF is:

    measured  >  supplier_actual  >  national  >  cbam_default  >  ipcc_default
"""
from __future__ import annotations

from .estimators import EstimatedValue


_TIER_ORDER = {
    "measured":         0,
    "supplier_actual":  1,
    "national":         2,
    "cbam_default":     3,
    "ipcc_default":     4,
    "estimated":        5,
}


def resolve(*candidates: EstimatedValue | None) -> EstimatedValue:
    """Pick the highest-priority non-null candidate. Falls back to the last
    candidate if all are None (caller's responsibility to always provide a
    default tail)."""
    real = [c for c in candidates if c is not None]
    if not real:
        raise ValueError("resolve() needs at least one non-null candidate")
    real.sort(key=lambda c: _TIER_ORDER.get(c.tier, 99))
    return real[0]
