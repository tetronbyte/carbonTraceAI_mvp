"""Run the CBAM calculation engine against whatever is in the canonical store.

  python -m scripts.run_calculation              # latest quarter, default config
  python -m scripts.run_calculation 2026-Q2      # specific quarter

Writes three artefacts to data/reports/:
  - cbam_quarterly_<run_id>.xml       (EU CBAM IT-Tools shape)
  - cbam_quarterly_<run_id>.csv       (flat one-row-per-product, dashboard-ready)
  - dashboard_<run_id>.json           (pre-aggregated JSON for the UI)
"""
from __future__ import annotations

import argparse
from pathlib import Path

from src.calculation import CBAMCalculationEngine, write_all
from src.storage.repository import Repository
from src.utils.logger import get_logger

log = get_logger(__name__)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("quarter", nargs="?", default=None, help="e.g. 2026-Q2")
    p.add_argument("--out", default="data/reports", help="output directory")
    args = p.parse_args()

    repo = Repository()
    engine = CBAMCalculationEngine(repo)
    run = engine.run(quarter=args.quarter)

    out_dir = Path(args.out)
    paths = write_all(run, out_dir)

    # Friendly summary
    print()
    print(f"CBAM run {run.run_id}")
    print(f"  facilities       : {len(run.facility_reports)}")
    print(f"  total products   : {sum(len(fr.products) for fr in run.facility_reports)}")
    for fr in run.facility_reports:
        print(f"  • {fr.facility_id} [{fr.quarter}]  "
              f"total={fr.total_emissions_tco2e:,.0f} tCO2e  "
              f"CBAM cost=€{fr.projected_cbam_cost_eur:,.0f}  "
              f"flagged_products={len(fr.products_over_estimation_threshold)}")
        for prod in fr.products:
            print(f"      ↳ CN {prod.product_cn_code}  out={prod.output_tonnes:,.0f}t  "
                  f"SEE={prod.total_see_tco2_per_t:.3f}  "
                  f"adj={prod.adjusted_see_tco2_per_t:.3f}  "
                  f"±{prod.overall_uncertainty_pct:.1f}%  "
                  f"est-share={prod.share_of_estimated_emissions*100:.1f}%")
    print()
    print("Artefacts:")
    for kind, path in paths.items():
        print(f"  {kind}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
