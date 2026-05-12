"""Renderers for downstream consumption.

  - cbam_xml() — EU CBAM IT-Tools quarterly report schema (simplified but
                 schema-shaped; the official XSD slots in 1:1 when published).
  - cbam_csv() — flat CSV one row per (facility × product × period) for
                 dashboard ingestion.
  - dashboard_json() — JSON pre-aggregated for the dashboard layer.
"""
from __future__ import annotations

import csv
import io
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from .result_models import CalculationRun, FacilityReport, ProductEmissions


# ---------------------------------------------------------------------------
# CBAM XML — quarterly report
# ---------------------------------------------------------------------------

CBAM_NS = "urn:eu:cbam:quarterly-report:v1"


def cbam_xml(run: CalculationRun) -> str:
    """Returns a CBAM-shaped XML string. The structure follows the public
    quarterly-report template (Annex I of CBAM IR 2023/1773)."""
    root = ET.Element(f"{{{CBAM_NS}}}QuarterlyReport", attrib={"runId": run.run_id})
    for fr in run.facility_reports:
        _facility_xml(root, fr)
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def _facility_xml(root: ET.Element, fr: FacilityReport) -> None:
    f = ET.SubElement(root, "Installation")
    ET.SubElement(f, "OperatorName").text = fr.legal_entity_name
    ET.SubElement(f, "FacilityId").text = fr.facility_id
    if fr.cbam_installation_id:
        ET.SubElement(f, "CbamInstallationId").text = fr.cbam_installation_id
    if fr.eori:
        ET.SubElement(f, "EORI").text = fr.eori
    if fr.un_locode:
        ET.SubElement(f, "UNLOCODE").text = fr.un_locode
    ET.SubElement(f, "Country").text = fr.country
    ET.SubElement(f, "Sector").text = fr.sector
    ET.SubElement(f, "Quarter").text = fr.quarter
    ET.SubElement(f, "ReportingPeriodStart").text = fr.reporting_period_start.isoformat()
    ET.SubElement(f, "ReportingPeriodEnd").text = fr.reporting_period_end.isoformat()

    g = ET.SubElement(f, "Goods")
    for p in fr.products:
        _product_xml(g, p)

    rollup = ET.SubElement(f, "Totals")
    ET.SubElement(rollup, "DirectEmissionsTCO2e").text = f"{fr.total_direct_tco2e:.3f}"
    ET.SubElement(rollup, "IndirectEmissionsTCO2e").text = f"{fr.total_indirect_tco2e:.3f}"
    ET.SubElement(rollup, "PrecursorEmissionsTCO2e").text = f"{fr.total_precursor_tco2e:.3f}"
    ET.SubElement(rollup, "TotalEmissionsTCO2e").text = f"{fr.total_emissions_tco2e:.3f}"
    ET.SubElement(rollup, "ProjectedCBAMCostEUR").text = f"{fr.projected_cbam_cost_eur:.2f}"

    recon = ET.SubElement(f, "Reconciliation")
    if fr.mass_balance_residual_pct is not None:
        ET.SubElement(recon, "MassBalanceResidualPct").text = f"{fr.mass_balance_residual_pct:.2f}"
    if fr.energy_balance_residual_pct is not None:
        ET.SubElement(recon, "EnergyBalanceResidualPct").text = f"{fr.energy_balance_residual_pct:.2f}"

    if fr.products_over_estimation_threshold:
        flags = ET.SubElement(f, "EstimationFlags")
        for cn in fr.products_over_estimation_threshold:
            ET.SubElement(flags, "ProductOver20pctEstimated").text = cn


def _product_xml(parent: ET.Element, p: ProductEmissions) -> None:
    g = ET.SubElement(parent, "Good", attrib={"cnCode": p.product_cn_code})
    ET.SubElement(g, "ProductName").text = p.product_name
    ET.SubElement(g, "OutputTonnes").text = f"{p.output_tonnes:.3f}"
    ET.SubElement(g, "EUExportTonnes").text = f"{p.eu_export_tonnes:.3f}"
    ET.SubElement(g, "DomesticSalesTonnes").text = f"{p.domestic_sales_tonnes:.3f}"
    ee = ET.SubElement(g, "EmbeddedEmissions")
    ET.SubElement(ee, "DirectSEE").text = f"{p.direct_see_tco2_per_t:.4f}"
    ET.SubElement(ee, "IndirectSEE").text = f"{p.indirect_see_tco2_per_t:.4f}"
    ET.SubElement(ee, "TotalSEE").text = f"{p.total_see_tco2_per_t:.4f}"
    ET.SubElement(ee, "AdjustedSEE").text = f"{p.adjusted_see_tco2_per_t:.4f}"
    ET.SubElement(ee, "OverallUncertaintyPct").text = f"{p.overall_uncertainty_pct:.2f}"
    ET.SubElement(ee, "ShareOfEstimatedEmissions").text = f"{p.share_of_estimated_emissions:.4f}"
    ET.SubElement(g, "CarbonPricePaidEURPerTCO2e").text = f"{p.carbon_price_paid_eur_per_tco2e:.4f}"
    ET.SubElement(g, "AllocationMethod").text = p.coproduct_allocation_method
    ET.SubElement(g, "AllocationShare").text = f"{p.allocation_share:.4f}"
    breakdown = ET.SubElement(g, "EmissionLines")
    for line in (*p.direct_lines, *p.indirect_lines, *p.precursor_lines):
        l = ET.SubElement(breakdown, "Line", attrib={
            "category": line.category,
            "tier": line.ef_tier,
            "estimated": "true" if line.is_estimated else "false",
        })
        ET.SubElement(l, "Label").text = line.label
        ET.SubElement(l, "Activity").text = f"{line.activity_value:.3f} {line.activity_unit}"
        ET.SubElement(l, "EF").text = f"{line.ef_value:.4f} {line.ef_unit}"
        ET.SubElement(l, "EFSource").text = line.ef_source
        ET.SubElement(l, "CO2eTonnes").text = f"{line.co2e_tonnes:.4f}"
        ET.SubElement(l, "UncertaintyPct").text = f"{line.uncertainty_pct:.2f}"


# ---------------------------------------------------------------------------
# CSV — flat one-row-per-product for dashboards
# ---------------------------------------------------------------------------

CSV_COLUMNS = [
    "run_id", "quarter", "facility_id", "country", "sector",
    "cn_code", "product_name",
    "output_tonnes", "eu_export_tonnes", "domestic_sales_tonnes",
    "direct_tco2e", "indirect_tco2e", "precursor_tco2e",
    "direct_see", "indirect_see", "total_see", "adjusted_see",
    "overall_uncertainty_pct", "share_estimated",
    "carbon_price_paid_eur", "eua_price_eur",
    "allocation_method", "allocation_share",
    "cbam_certificate_cost_eur",
]


def cbam_csv(run: CalculationRun) -> str:
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=CSV_COLUMNS)
    w.writeheader()
    for fr in run.facility_reports:
        for p in fr.products:
            w.writerow({
                "run_id": run.run_id,
                "quarter": fr.quarter,
                "facility_id": fr.facility_id,
                "country": fr.country,
                "sector": fr.sector,
                "cn_code": p.product_cn_code,
                "product_name": p.product_name,
                "output_tonnes": round(p.output_tonnes, 3),
                "eu_export_tonnes": round(p.eu_export_tonnes, 3),
                "domestic_sales_tonnes": round(p.domestic_sales_tonnes, 3),
                "direct_tco2e": round(p.direct_emissions_tco2e, 3),
                "indirect_tco2e": round(p.indirect_emissions_tco2e, 3),
                "precursor_tco2e": round(p.precursor_emissions_tco2e, 3),
                "direct_see": round(p.direct_see_tco2_per_t, 4),
                "indirect_see": round(p.indirect_see_tco2_per_t, 4),
                "total_see": round(p.total_see_tco2_per_t, 4),
                "adjusted_see": round(p.adjusted_see_tco2_per_t, 4),
                "overall_uncertainty_pct": round(p.overall_uncertainty_pct, 2),
                "share_estimated": round(p.share_of_estimated_emissions, 4),
                "carbon_price_paid_eur": round(p.carbon_price_paid_eur_per_tco2e, 4),
                "eua_price_eur": p.eua_price_eur_per_tco2e,
                "allocation_method": p.coproduct_allocation_method,
                "allocation_share": round(p.allocation_share, 4),
                "cbam_certificate_cost_eur": round(p.cbam_certificate_cost_eur, 2),
            })
    return out.getvalue()


# ---------------------------------------------------------------------------
# Dashboard JSON
# ---------------------------------------------------------------------------

def dashboard_json(run: CalculationRun) -> str:
    """Pre-aggregated JSON for the dashboard layer.

    Top-level structure:
      runId, generatedAt,
      facilities: [{
        facilityId, country, sector, quarter,
        totals: {direct, indirect, precursor, total, projectedCBAMCostEUR},
        products: [{cn, name, output_t, eu_export_t, totalSEE, adjustedSEE, uncertaintyPct, ...}],
        timeSeries: {emissionsByMonth: {...}}  # populated by aggregator if monthly
      }]
    """
    payload = {
        "runId": run.run_id,
        "generatedAt": run.finished_at,
        "facilities": [
            {
                "facilityId": fr.facility_id,
                "name": fr.legal_entity_name,
                "country": fr.country,
                "sector": fr.sector,
                "quarter": fr.quarter,
                "totals": {
                    "directTCO2e": fr.total_direct_tco2e,
                    "indirectTCO2e": fr.total_indirect_tco2e,
                    "precursorTCO2e": fr.total_precursor_tco2e,
                    "totalTCO2e": fr.total_emissions_tco2e,
                    "projectedCBAMCostEUR": fr.projected_cbam_cost_eur,
                    "euExportShare": fr.eu_export_share,
                },
                "reconciliation": {
                    "massBalanceResidualPct": fr.mass_balance_residual_pct,
                    "energyBalanceResidualPct": fr.energy_balance_residual_pct,
                    "financeResidualPct": fr.finance_cross_check_residual_pct,
                },
                "estimationFlags": fr.products_over_estimation_threshold,
                "products": [_product_json(p) for p in fr.products],
            }
            for fr in run.facility_reports
        ],
    }
    return json.dumps(payload, indent=2)


def _product_json(p: ProductEmissions) -> dict:
    return {
        "cn": p.product_cn_code,
        "name": p.product_name,
        "outputT": p.output_tonnes,
        "euExportT": p.eu_export_tonnes,
        "directSEE": p.direct_see_tco2_per_t,
        "indirectSEE": p.indirect_see_tco2_per_t,
        "totalSEE": p.total_see_tco2_per_t,
        "adjustedSEE": p.adjusted_see_tco2_per_t,
        "uncertaintyPct": p.overall_uncertainty_pct,
        "shareEstimated": p.share_of_estimated_emissions,
        "carbonPricePaidEUR": p.carbon_price_paid_eur_per_tco2e,
        "cbamCostEUR": p.cbam_certificate_cost_eur,
        "allocation": {"method": p.coproduct_allocation_method, "share": p.allocation_share},
        "lines": [
            {
                "category": l.category, "label": l.label,
                "activity": l.activity_value, "activityUnit": l.activity_unit,
                "ef": l.ef_value, "efUnit": l.ef_unit,
                "tier": l.ef_tier, "source": l.ef_source,
                "co2e": l.co2e_tonnes, "uncertaintyPct": l.uncertainty_pct,
                "estimated": l.is_estimated,
            }
            for l in (*p.direct_lines, *p.indirect_lines, *p.precursor_lines)
        ],
    }


# ---------------------------------------------------------------------------
# Convenience: write all three to disk
# ---------------------------------------------------------------------------

def write_all(run: CalculationRun, out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "xml":  out_dir / f"cbam_quarterly_{run.run_id}.xml",
        "csv":  out_dir / f"cbam_quarterly_{run.run_id}.csv",
        "json": out_dir / f"dashboard_{run.run_id}.json",
    }
    paths["xml"].write_text(cbam_xml(run))
    paths["csv"].write_text(cbam_csv(run))
    paths["json"].write_text(dashboard_json(run))
    return paths
