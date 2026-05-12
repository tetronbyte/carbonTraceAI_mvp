"""CBAM calculation engine — orchestrates lookup → aggregation → formulas →
allocation → adjustment → reconciliation → result.

Public surface:
    CBAMCalculationEngine(repository).run(quarter="2026-Q2") → CalculationRun

The engine reads canonical Pydantic payloads from `Repository` (the same store
the ingestion pipeline writes to), so no other module needs to know about
SQLite or Frappe doctypes.
"""
from __future__ import annotations

import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from src.core.enums import AllocationMethod
from src.storage.repository import Repository
from src.utils.logger import get_logger

from . import estimators as est
from . import formulas as F
from . import lookup_tables as lut
from .aggregation import (
    AggregatedActivity,
    aggregate_by_quarter,
    quarter_bounds,
    quarter_of,
)
from .allocation import allocation_share
from .carbon_price import carbon_price_paid_eur_per_tco2e
from .reconciliation import energy_balance, finance_cross_check, mass_balance
from .result_models import (
    CalculationRun,
    EmissionLine,
    FacilityReport,
    ProductEmissions,
)
from .uncertainty import Uncertainty, combine_additive, share_estimated

log = get_logger(__name__)


# CN code → fuel type (used to look up IPCC defaults for fuels bought via PO).
_FUEL_BY_CN = {
    "27112100": "natural_gas",   # natural gas
    "27101941": "diesel",
    "27101962": "heavy_fuel_oil",
    "27111200": "lpg",
    "25030000": None,            # sulphur — not a fuel for combustion
}

# Material name → fuel type (fallback when CN missing)
_FUEL_BY_NAME = {
    "natural_gas": "natural_gas", "nat-gas": "natural_gas",
    "natural_gas_fs": "natural_gas", "nat-gas-fs": "natural_gas",
    "natural_gas_fuel": "natural_gas", "nat-gas-fuel": "natural_gas",
    "diesel": "diesel", "heavy_fuel_oil": "heavy_fuel_oil", "hfo": "heavy_fuel_oil",
    "lpg": "lpg",
}


@dataclass
class EngineConfig:
    eua_price_eur_per_tco2e: float = lut.EUA_PRICE_EUR_PER_TCO2E
    gwp_set: str = "AR6"
    coproduct_method: AllocationMethod = AllocationMethod.MASS
    mass_balance_tolerance_pct: float = 5.0
    energy_balance_tolerance_pct: float = 10.0


class CBAMCalculationEngine:
    def __init__(self, repository: Repository, config: Optional[EngineConfig] = None) -> None:
        self.repository = repository
        self.cfg = config or EngineConfig()

    # ---- public entrypoint ---------------------------------------------------
    def run(self, quarter: str | None = None) -> CalculationRun:
        run_id = str(uuid.uuid4())
        started = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
        log.info("CBAM calc engine starting — run_id=%s quarter=%s", run_id, quarter)

        # Pull all canonical payloads once
        production = self.repository.fetch_payloads("production_runs")
        facilities = self.repository.fetch_payloads("facilities")
        energy = self.repository.fetch_payloads("energy_consumption")
        precursors = self.repository.fetch_payloads("precursor_purchases")
        aluminium_recs = self.repository.fetch_payloads("aluminium_process")
        fertiliser_recs = self.repository.fetch_payloads("fertiliser_process")
        fugitive = self.repository.fetch_payloads("fugitive_emissions")
        recs = self._safe_fetch("recs_certificates")
        carbon_prices = self._safe_fetch("carbon_price_paid")

        # Auto-pick quarter from data if not supplied
        if quarter is None and production:
            quarter = quarter_of(max(_d(p["run_started_at"]) for p in production))
        quarter = quarter or quarter_of(datetime.utcnow().date())

        facility_ids = sorted({p["facility_id"] for p in production} or {f.get("id") for f in facilities})
        facility_reports: list[FacilityReport] = []
        for fid in facility_ids:
            f_row = next((f for f in facilities if f.get("id") == fid or fid in (f.get("legal_entity_name") or "")), None) \
                    or next((f for f in facilities if f.get("country")), None)
            if not f_row:
                continue
            fr = self._compute_facility(
                fid, quarter, f_row,
                production, energy, precursors, aluminium_recs,
                fertiliser_recs, fugitive, recs, carbon_prices,
            )
            facility_reports.append(fr)

        run = CalculationRun(
            run_id=run_id,
            started_at=started,
            finished_at=datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
            facility_reports=facility_reports,
        )
        log.info("CBAM calc engine done — %s facilities, %s products",
                 len(facility_reports), sum(len(fr.products) for fr in facility_reports))
        return run

    # ---- per-facility --------------------------------------------------------
    def _compute_facility(
        self, facility_id, quarter, facility_row,
        production, energy, precursors, al_recs, fert_recs,
        fugitive, recs, carbon_prices,
    ) -> FacilityReport:
        q_start, q_end = quarter_bounds(quarter)
        buckets = aggregate_by_quarter(
            facility_id, quarter,
            production, energy, precursors,
            al_recs, fert_recs, fugitive, recs, carbon_prices,
        )

        # carbon price paid (Block G) is facility-level — compute once
        cp_eur = carbon_price_paid_eur_per_tco2e(
            [c for c in carbon_prices if c.get("facility_id") == facility_id
             and self._in_q(c.get("period_start"), q_start, q_end)]
        )

        product_emissions: list[ProductEmissions] = []
        all_outputs_t: dict[str, float] = {b.cn_code: b.total_output_t for b in buckets.values()}
        for cn, bucket in buckets.items():
            if bucket.total_output_t <= 0:
                continue
            p = self._compute_product(bucket, facility_row, cp_eur, all_outputs_t)
            product_emissions.append(p)

        fr = FacilityReport(
            facility_id=facility_id,
            legal_entity_name=facility_row.get("legal_entity_name", facility_id),
            country=facility_row.get("country", "??"),
            sector=facility_row.get("sector", "?"),
            cbam_installation_id=facility_row.get("cbam_installation_id"),
            un_locode=facility_row.get("un_locode"),
            eori=facility_row.get("eori"),
            reporting_period_start=q_start,
            reporting_period_end=q_end,
            quarter=quarter,
            products=product_emissions,
        )
        self._rollup(fr)
        return fr

    # ---- per-product (the heart of the engine) ------------------------------
    def _compute_product(
        self,
        bucket: AggregatedActivity,
        facility_row: dict,
        cp_eur: float,
        all_outputs_t: dict[str, float],
    ) -> ProductEmissions:
        cn = bucket.cn_code
        output_t = bucket.total_output_t
        eu_export_t = bucket.eu_export_t
        domestic_t = output_t - eu_export_t

        # ---- direct emissions ----
        direct_lines: list[EmissionLine] = []
        # 1. Fuel combustion (PO-derived rows that the ERP mapper tagged as fuel)
        for fc in bucket.fuel_consumption:
            line = self._fuel_line(fc)
            if line:
                direct_lines.append(line)
        # 2. Process emissions — aluminium-specific
        for r in bucket.process_records_al:
            direct_lines.extend(self._aluminium_process_lines(r))
        # 3. Process emissions — fertiliser-specific
        for r in bucket.process_records_fert:
            direct_lines.extend(self._fertiliser_process_lines(r))
        # 4. Fugitive emissions (allocated by mass share across CNs)
        cn_share = output_t / max(sum(all_outputs_t.values()), 1e-9)
        for f in bucket.fugitive:
            direct_lines.extend(self._fugitive_lines(f, cn_share))

        # ---- indirect emissions ----
        indirect_lines: list[EmissionLine] = []
        country = facility_row.get("country", "MZ")
        for e in bucket.electricity_consumption:
            indirect_lines.append(self._electricity_line(e, country))
        for s in bucket.steam_consumption:
            indirect_lines.append(self._steam_line(s))
        # subtract MWh of RECs / GOs retired against this CN's share
        recs_mwh = sum(r.get("mwh", 0) for r in bucket.recs) * cn_share
        if recs_mwh > 0 and indirect_lines:
            # apply REC reduction proportionally to grid-electricity lines
            total_kwh = sum(l.activity_value for l in indirect_lines
                            if l.category == "electricity")
            if total_kwh > 0:
                reduction_factor = max(0.0, 1 - (recs_mwh * 1000 / total_kwh))
                for line in indirect_lines:
                    if line.category == "electricity":
                        line_dict = line.model_dump()
                        line_dict["co2e_tonnes"] = line.co2e_tonnes * reduction_factor
                        line_dict["label"] = f"{line.label} (REC-adjusted)"
                        indirect_lines[indirect_lines.index(line)] = EmissionLine(**line_dict)

        # ---- precursor (complex-goods) emissions ----
        precursor_lines: list[EmissionLine] = []
        for p in bucket.precursors:
            precursor_lines.append(F.precursor_line(
                cn_code=p.get("precursor_cn_code") or "00000000",
                quantity_tonnes=float(p.get("quantity_tonnes", 0)),
                ee=est.estimate_precursor_ee(
                    p.get("precursor_cn_code") or "00000000",
                    supplier_actual=p.get("embedded_emissions_tco2_per_t")
                    if p.get("ee_method") == "actual" else None,
                ),
            ))

        # ---- totals + SEE ----
        direct_t = sum(l.co2e_tonnes for l in direct_lines)
        indirect_t = sum(l.co2e_tonnes for l in indirect_lines)
        precursor_t = sum(l.co2e_tonnes for l in precursor_lines)
        direct_see, indirect_see, total_see = F.specific_embedded_emissions(
            direct_t, indirect_t, precursor_t, output_t,
        )
        adjusted = F.adjusted_see(total_see, cp_eur, self.cfg.eua_price_eur_per_tco2e)
        cbam_cost = F.cbam_certificate_cost_eur(
            adjusted, eu_export_t, self.cfg.eua_price_eur_per_tco2e,
        )

        # ---- uncertainty rollup ----
        all_lines = direct_lines + indirect_lines + precursor_lines
        unc_components = [Uncertainty(l.co2e_tonnes, l.uncertainty_pct) for l in all_lines]
        unc_total = combine_additive(unc_components)
        est_lines = [u for u, l in zip(unc_components, all_lines) if l.is_estimated]
        share_est = share_estimated(unc_components, est_lines)

        # ---- coproduct allocation share (used in dashboards) ----
        share = allocation_share(all_outputs_t, cn) if self.cfg.coproduct_method != AllocationMethod.NONE else 1.0

        return ProductEmissions(
            facility_id=bucket.facility_id,
            product_cn_code=cn,
            product_name=_product_name_for_cn(cn),
            period_start=quarter_bounds(bucket.quarter)[0],
            period_end=quarter_bounds(bucket.quarter)[1],
            output_tonnes=output_t,
            eu_export_tonnes=eu_export_t,
            domestic_sales_tonnes=domestic_t,
            direct_emissions_tco2e=direct_t,
            direct_lines=direct_lines,
            indirect_emissions_tco2e=indirect_t,
            indirect_lines=indirect_lines,
            precursor_emissions_tco2e=precursor_t,
            precursor_lines=precursor_lines,
            direct_see_tco2_per_t=direct_see,
            indirect_see_tco2_per_t=indirect_see,
            total_see_tco2_per_t=total_see,
            adjusted_see_tco2_per_t=adjusted,
            overall_uncertainty_pct=unc_total.pct,
            share_of_estimated_emissions=share_est,
            carbon_price_paid_eur_per_tco2e=cp_eur,
            eua_price_eur_per_tco2e=self.cfg.eua_price_eur_per_tco2e,
            coproduct_allocation_method=self.cfg.coproduct_method.value,
            allocation_share=share,
            cbam_certificate_cost_eur=cbam_cost,
        )

    # ---- emission-line factories --------------------------------------------
    def _fuel_line(self, fc: dict) -> Optional[EmissionLine]:
        ft = self._resolve_fuel_type(fc)
        if not ft:
            return None
        qty = float(fc.get("quantity", 0))
        if qty <= 0:
            return None
        unit = fc.get("unit", "tonnes")
        ncv = est.estimate_ncv(ft, measured=fc.get("ncv_gj_per_tonne"))
        # For gases priced per 1000 Nm3, scale activity to thousands
        activity = qty / 1000.0 if unit == "Nm3" else qty
        activity_unit = "1000 Nm3" if unit == "Nm3" else unit
        ef = est.estimate_fuel_ef_kg_co2_per_gj(ft)
        ox = est.estimate_oxidation_factor(ft, fc.get("oxidation_factor"))
        return F.fuel_combustion_emissions_t(
            activity_value=activity, activity_unit=activity_unit,
            ncv=ncv, ef_kg_per_gj=ef, oxidation=ox,
            label=f"{ft} ({fc.get('supplier_name') or 'unknown'})",
        )

    @staticmethod
    def _resolve_fuel_type(fc: dict) -> Optional[str]:
        if (fuel := fc.get("fuel_type")):
            return str(fuel).lower()
        # PO mapper sets material on supplier_name sometimes — try a name match
        for key, ft in _FUEL_BY_NAME.items():
            if key in str(fc.get("supplier_name", "")).lower():
                return ft
        meter = str(fc.get("meter_type", "")).lower()
        if "natural_gas" in meter:
            return "natural_gas"
        if "diesel" in meter:
            return "diesel"
        return None

    def _aluminium_process_lines(self, r: dict) -> list[EmissionLine]:
        out: list[EmissionLine] = []
        anode_t = float(r.get("anode_consumption_tonnes", 0))
        if anode_t > 0:
            ev = est.estimate_anode_co2_t(anode_t)
            out.append(F.process_emission_line(
                "Pre-bake anode CO2", ev, anode_t, "tonnes",
            ))
        al_t = float(r.get("primary_al_output_tonnes", 0))
        if al_t > 0:
            ae_min = r.get("anode_effect_minutes")
            pfc = est.estimate_pfc_co2e_t(
                al_tonnes=al_t,
                route="PRIMARY_PREBAKE",
                anode_effect_minutes_per_pot_day=ae_min,
                gwp_set=self.cfg.gwp_set,
            )
            out.append(F.process_emission_line("PFCs (CF4 + C2F6)", pfc, al_t, "tonnes Al"))
        return out

    def _fertiliser_process_lines(self, r: dict) -> list[EmissionLine]:
        out: list[EmissionLine] = []
        ng = float(r.get("feedstock_natural_gas_nm3", 0))
        if ng > 0:
            ev = est.estimate_nh3_smr_process_co2_t(ng)
            # net the captured CO2 used for urea (in‐facility)
            urea_t = float(r.get("urea_production_tonnes", 0))
            captured = float(r.get("co2_captured_tco2", 0))
            adjusted = ev.value - captured  # captured CO2 doesn't go to atmosphere
            ev2 = est.EstimatedValue(max(0.0, adjusted), ev.uncertainty_pct, ev.tier,
                                     ev.source + " (net of capture)")
            out.append(F.process_emission_line("NH3 SMR process CO2", ev2, ng, "Nm3"))
        hno3_t = float(r.get("nitric_acid_production_tonnes", 0))
        if hno3_t > 0:
            ev = est.estimate_hno3_n2o_tco2e(hno3_t, gwp_set=self.cfg.gwp_set)
            out.append(F.process_emission_line("HNO3 N2O", ev, hno3_t, "tonnes HNO3"))
        return out

    def _fugitive_lines(self, f: dict, cn_share: float) -> list[EmissionLine]:
        out: list[EmissionLine] = []
        if f.get("refrigerant_type") and f.get("refrigerant_topup_kg", 0) > 0:
            ev = est.estimate_refrigerant_co2e_t(
                f["refrigerant_type"], float(f["refrigerant_topup_kg"]) * cn_share,
                gwp_set=self.cfg.gwp_set,
            )
            out.append(F.process_emission_line(
                f"Refrigerant {f['refrigerant_type']}", ev,
                float(f["refrigerant_topup_kg"]) * cn_share, "kg",
            ))
        if f.get("sf6_topup_kg", 0) > 0:
            ev = est.estimate_sf6_co2e_t(float(f["sf6_topup_kg"]) * cn_share,
                                         gwp_set=self.cfg.gwp_set)
            out.append(F.process_emission_line(
                "SF6 leakage", ev, float(f["sf6_topup_kg"]) * cn_share, "kg",
            ))
        if f.get("flaring_nm3", 0) > 0:
            ev = est.estimate_flaring_co2e_t(
                float(f["flaring_nm3"]) * cn_share,
                ch4_pct=f.get("flare_gas_ch4_pct"),
                combustion_efficiency=f.get("flare_combustion_efficiency", 0.98),
                gwp_set=self.cfg.gwp_set,
            )
            out.append(F.process_emission_line(
                "Flaring", ev, float(f["flaring_nm3"]) * cn_share, "Nm3",
            ))
        return out

    def _electricity_line(self, e: dict, country: str) -> EmissionLine:
        kwh = float(e.get("quantity", 0))
        if e.get("unit") == "MWh":
            kwh *= 1000
        grid_ef = est.estimate_grid_ef(country, e.get("grid_emission_factor_kgco2_per_kwh"))
        return F.electricity_emissions_t(kwh, grid_ef,
                                          label=f"Electricity ({e.get('cost_centre') or 'site'})")

    def _steam_line(self, s: dict) -> EmissionLine:
        gj = float(s.get("quantity", 0))
        if s.get("unit") == "tonnes":  # 1 t steam ≈ 2.7 GJ
            gj *= 2.7
        steam_ef = est.estimate_steam_ef()
        return F.steam_emissions_t(gj, steam_ef)

    # ---- roll-up + reconciliation -------------------------------------------
    def _rollup(self, fr: FacilityReport) -> None:
        fr.total_direct_tco2e = sum(p.direct_emissions_tco2e for p in fr.products)
        fr.total_indirect_tco2e = sum(p.indirect_emissions_tco2e for p in fr.products)
        fr.total_precursor_tco2e = sum(p.precursor_emissions_tco2e for p in fr.products)
        fr.total_emissions_tco2e = fr.total_direct_tco2e + fr.total_indirect_tco2e + fr.total_precursor_tco2e
        fr.projected_cbam_cost_eur = sum(p.cbam_certificate_cost_eur for p in fr.products)
        total_out = sum(p.output_tonnes for p in fr.products) or 1.0
        fr.eu_export_share = sum(p.eu_export_tonnes for p in fr.products) / total_out
        fr.products_over_estimation_threshold = [
            p.product_cn_code for p in fr.products if p.share_of_estimated_emissions > 0.20
        ]
        if not fr.products:
            fr.missing_data_warnings.append("No production runs in this period")
        # mass-balance: precursor input vs output × BOM ratio (proxy: 1.0 if no precursors)
        for p in fr.products:
            if p.precursor_emissions_tco2e == 0:
                fr.missing_data_warnings.append(
                    f"No precursor data for CN {p.product_cn_code} — defaulted to 0"
                )

    # ---- helpers -------------------------------------------------------------
    def _safe_fetch(self, table: str) -> list[dict]:
        try:
            return self.repository.fetch_payloads(table)
        except Exception:
            return []

    @staticmethod
    def _in_q(d_str, q_start, q_end) -> bool:
        if not d_str:
            return False
        from datetime import date as _date
        try:
            d = _date.fromisoformat(str(d_str)[:10])
        except ValueError:
            return False
        return q_start <= d <= q_end


def _d(v):
    from datetime import date as _date, datetime as _dt
    if isinstance(v, _date):
        return v
    return _dt.fromisoformat(str(v).replace("Z", "+00:00")).date()


_CN_PRODUCT_NAMES = {
    "76011000": "Primary Aluminium Ingot",
    "76012000": "Aluminium Alloy",
    "28141000": "Anhydrous Ammonia",
    "31021010": "Prilled Urea",
    "28080000": "Nitric Acid",
    "31053000": "Di-ammonium Phosphate",
}


def _product_name_for_cn(cn: str) -> str:
    return _CN_PRODUCT_NAMES.get(cn, f"Product {cn}")
