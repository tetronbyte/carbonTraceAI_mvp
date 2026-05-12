"""Uncertainty propagation per CBAM MRV uncertainty guidance.

For independent additive emission components (Σ aE_i) — combine RSS:

  σ_total = sqrt( Σ (σ_i × E_i)^2 ) / Σ E_i

For ratio-like products (NCV × EF × OF), combine RSS on the relative
uncertainties.

The calc engine attaches an `Uncertainty` to every emission line so the final
SEE has a defensible ±% band for the verifier.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class Uncertainty:
    value: float                # the central estimate
    pct: float                  # ± as percent
    @property
    def absolute(self) -> float:
        return abs(self.value) * (self.pct / 100.0)


def combine_relative(*pcts: float) -> float:
    """Combine independent relative uncertainties in quadrature."""
    return sqrt(sum((p or 0) ** 2 for p in pcts))


def combine_additive(lines: list[Uncertainty]) -> Uncertainty:
    """Combine additive emission components by root-sum-square of absolutes."""
    total = sum(l.value for l in lines)
    if not lines or total == 0:
        return Uncertainty(0.0, 0.0)
    abs_var = sqrt(sum(l.absolute ** 2 for l in lines))
    return Uncertainty(total, (abs_var / abs(total)) * 100.0 if total else 0.0)


def share_estimated(lines: list[Uncertainty], estimated_lines: list[Uncertainty]) -> float:
    """Return the share of total emissions that comes from estimated sources.
    CBAM IR Art.4(3) caps this at 20% for complex goods in the transitional period."""
    total = sum(l.value for l in lines) or 1.0
    est = sum(l.value for l in estimated_lines)
    return est / total
