"""Reconciliation checks the verifier expects to see:

  1. Mass balance      — Σ precursor inputs ≈ Σ outputs × BOM ratio (±5% tolerance)
  2. Energy balance    — Σ fuel energy ≈ process heat demand + losses
  3. Finance cross     — Σ GL fuel cost ≈ Σ PO unit_price × qty (within ±2%)

Each check produces a residual % which lands on the FacilityReport.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReconciliationResult:
    name: str
    inputs: float
    outputs: float
    residual_pct: float
    passes: bool
    tolerance_pct: float


def mass_balance(
    inputs_t: float, expected_t: float, tolerance_pct: float = 5.0,
) -> ReconciliationResult:
    if expected_t <= 0:
        return ReconciliationResult("mass_balance", inputs_t, expected_t, 0.0, True, tolerance_pct)
    residual = abs(inputs_t - expected_t) / expected_t * 100.0
    return ReconciliationResult(
        "mass_balance", inputs_t, expected_t, residual,
        residual <= tolerance_pct, tolerance_pct,
    )


def energy_balance(
    fuel_energy_gj: float, expected_gj: float, tolerance_pct: float = 10.0,
) -> ReconciliationResult:
    if expected_gj <= 0:
        return ReconciliationResult("energy_balance", fuel_energy_gj, expected_gj, 0.0, True, tolerance_pct)
    residual = abs(fuel_energy_gj - expected_gj) / expected_gj * 100.0
    return ReconciliationResult(
        "energy_balance", fuel_energy_gj, expected_gj, residual,
        residual <= tolerance_pct, tolerance_pct,
    )


def finance_cross_check(
    gl_cost: float, po_cost: float, tolerance_pct: float = 2.0,
) -> ReconciliationResult:
    if po_cost <= 0:
        return ReconciliationResult("finance_cross", gl_cost, po_cost, 0.0, True, tolerance_pct)
    residual = abs(gl_cost - po_cost) / po_cost * 100.0
    return ReconciliationResult(
        "finance_cross", gl_cost, po_cost, residual,
        residual <= tolerance_pct, tolerance_pct,
    )
