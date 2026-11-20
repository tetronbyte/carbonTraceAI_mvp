"""In-process pipeline job runner.

For the demo we keep state in memory — a dict of run_id → JobState. Production
would swap this for Redis + RQ. The contract the frontend depends on:

  POST /api/runs                  → creates a job, returns run_id
  GET  /api/runs/{run_id}/status  → polls progress (steps + log lines)
  GET  /api/runs/{run_id}         → final dashboard JSON when status=succeeded
"""
from __future__ import annotations

import threading
import time
import traceback
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.calculation import CBAMCalculationEngine, EngineConfig, write_all
from src.calculation.aggregation import quarter_bounds, quarter_of
from src.calculation.lookup_tables import cbam_default
from src.ingestion.erp.erpnext_client import ERPNextClient, ERPNextCredentials
from src.ingestion.orchestrator import IngestionOrchestrator
from src.seeding import ERPNextSeeder, get_profile
from src.storage.repository import Repository
from src.utils.logger import get_logger

log = get_logger(__name__)


_PIPELINE_STEPS = (
    "connect_erp",
    "seed_erp",
    "pull_erp",
    "manual_supplement",
    "calculate",
    "render_reports",
)


@dataclass
class StepStatus:
    name: str
    state: str = "pending"          # pending | running | succeeded | failed | skipped
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    detail: str = ""


@dataclass
class JobState:
    run_id: str
    profile_key: str
    base_url: str
    started_at: str
    state: str = "queued"           # queued | running | succeeded | failed
    finished_at: Optional[str] = None
    error: Optional[str] = None
    steps: list[StepStatus] = field(default_factory=list)
    log_lines: list[str] = field(default_factory=list)
    artefacts: dict[str, str] = field(default_factory=dict)
    facility_id: Optional[str] = None
    seed_summary: Optional[dict] = None
    ingestion_summary: Optional[dict] = None
    calc_summary: Optional[dict] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "profile_key": self.profile_key,
            "base_url": self.base_url,
            "state": self.state,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "error": self.error,
            "facility_id": self.facility_id,
            "steps": [
                {"name": s.name, "state": s.state, "detail": s.detail,
                 "started_at": s.started_at, "finished_at": s.finished_at}
                for s in self.steps
            ],
            "log_tail": self.log_lines[-30:],
            "seed_summary": self.seed_summary,
            "ingestion_summary": self.ingestion_summary,
            "calc_summary": self.calc_summary,
            "artefacts": self.artefacts,
        }


_JOBS: dict[str, JobState] = {}
_JOBS_LOCK = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")


def list_jobs() -> list[JobState]:
    with _JOBS_LOCK:
        return sorted(_JOBS.values(), key=lambda j: j.started_at, reverse=True)


def get_job(run_id: str) -> Optional[JobState]:
    with _JOBS_LOCK:
        return _JOBS.get(run_id)


def create_job(
    *,
    profile_key: str,
    base_url: str,
    api_key: str,
    api_secret: str,
    seed_if_empty: bool = True,
    fast_demo: bool = True,
) -> JobState:
    run_id = str(uuid.uuid4())
    job = JobState(
        run_id=run_id,
        profile_key=profile_key,
        base_url=base_url,
        started_at=_now(),
        steps=[StepStatus(name=n) for n in _PIPELINE_STEPS],
    )
    with _JOBS_LOCK:
        _JOBS[run_id] = job

    thread = threading.Thread(
        target=_run_pipeline,
        args=(job, api_key, api_secret, seed_if_empty, fast_demo),
        daemon=True,
        name=f"pipeline-{run_id[:8]}",
    )
    thread.start()
    return job


def _emit(job: JobState, line: str) -> None:
    stamped = f"{_now()}  {line}"
    job.log_lines.append(stamped)
    log.info("[%s] %s", job.run_id[:8], line)


def _step(job: JobState, name: str) -> StepStatus:
    return next(s for s in job.steps if s.name == name)


def _begin(job: JobState, name: str) -> StepStatus:
    s = _step(job, name)
    s.state = "running"
    s.started_at = _now()
    _emit(job, f"▶ {name}")
    return s


def _succeed(job: JobState, s: StepStatus, detail: str = "") -> None:
    s.state = "succeeded"
    s.detail = detail
    s.finished_at = _now()
    _emit(job, f"✓ {s.name}{(' — ' + detail) if detail else ''}")


def _skip(job: JobState, name: str, detail: str = "") -> None:
    s = _step(job, name)
    s.state = "skipped"
    s.detail = detail
    s.started_at = s.finished_at = _now()
    _emit(job, f"↷ {name}{(' — ' + detail) if detail else ''}")


def _fail(job: JobState, s: StepStatus, err: str) -> None:
    s.state = "failed"
    s.detail = err
    s.finished_at = _now()
    _emit(job, f"✗ {s.name} — {err}")


def _run_pipeline(
    job: JobState, api_key: str, api_secret: str,
    seed_if_empty: bool, fast_demo: bool,
) -> None:
    job.state = "running"
    repo = Repository()
    creds = ERPNextCredentials(base_url=job.base_url, api_key=api_key, api_secret=api_secret)

    # 1. Connect
    s = _begin(job, "connect_erp")
    client = ERPNextClient(creds)
    try:
        if not client.ping():
            raise ConnectionError(f"ERPNext unreachable at {job.base_url}")
        _succeed(job, s, f"reachable at {job.base_url}")
    except Exception as e:
        _fail(job, s, str(e))
        job.state = "failed"; job.error = str(e); job.finished_at = _now()
        return

    profile = get_profile(job.profile_key)
    job.facility_id = profile.facility_code

    # 2. Seed (optional — skipped if ERPNext already has Work Orders)
    s = _begin(job, "seed_erp")
    try:
        already_seeded = client.get_count("Work Order", filters={"custom_facility_code": profile.facility_code}) > 0
        if already_seeded:
            _skip(job, "seed_erp", "already seeded")
        elif not seed_if_empty:
            _skip(job, "seed_erp", "seed_if_empty=False")
        else:
            seed_profile = profile
            if fast_demo:
                # Fast demo: 3 months × 12 WOs/month so the seeder finishes in
                # ~90 seconds instead of 10-25 min.
                seed_profile = type(profile)(**{**profile.__dict__,
                                                "months": 3,
                                                "work_orders_per_month": 12,
                                                "purchase_orders_per_month": 8})
            seeder = ERPNextSeeder(client, seed_profile, seed=42, invoice_ratio=0.5)
            report = seeder.run()
            job.seed_summary = {
                "items": report.items, "suppliers": report.suppliers,
                "customers": report.customers, "work_orders": report.work_orders,
                "purchase_orders": report.purchase_orders,
                "purchase_invoices": report.purchase_invoices,
                "stock_entries": report.stock_entries,
                "quality_inspections": report.quality_inspections,
                "sales_invoices": report.sales_invoices,
                "errors": len(report.errors),
            }
            for err in report.errors[:5]:
                _emit(job, f"seed error: {err[:300]}")
            errors_note = f" ({len(report.errors)} seed errors)" if report.errors else ""
            _succeed(job, s, f"{report.work_orders} WOs + {report.purchase_orders} POs + {report.sales_invoices} SInv{errors_note}")
    except Exception as e:
        _fail(job, s, str(e))
        job.state = "failed"; job.error = str(e); job.finished_at = _now()
        return

    # 3. Pull canonical streams
    s = _begin(job, "pull_erp")
    try:
        # Re-pull replaces this facility's rows; otherwise reruns double-count.
        removed = repo.clear_facility(profile.facility_code, legal_entity_name=profile.legal_name)
        if removed:
            _emit(job, f"cleared {removed} canonical rows from the previous run")
        orch = IngestionOrchestrator(repository=repo)
        orch.run_erpnext_direct(creds)
        events = [r.event for r in orch.report.results]
        job.ingestion_summary = {
            "events": [
                {"source": e.source.value if hasattr(e.source, "value") else str(e.source),
                 "stream": e.stream, "records": e.record_count,
                 "ok": e.ok_count, "errors": e.error_count}
                for e in events
            ],
            "total_records": sum(e.record_count for e in events),
        }
        _succeed(job, s, f"{job.ingestion_summary['total_records']} canonical rows")
    except Exception as e:
        _fail(job, s, str(e))
        job.state = "failed"; job.error = str(e); job.finished_at = _now()
        return

    # 4. Manual / supplier / OCR supplement (always-on for the demo)
    s = _begin(job, "manual_supplement")
    try:
        _succeed(job, s, _emit_demo_manual_supplements(job, orch, repo, profile))
    except Exception as e:
        _emit(job, f"manual_supplement warning: {e}\n{traceback.format_exc(limit=2)}")
        _succeed(job, s, "(partial) " + str(e))

    # 5. Calc engine
    s = _begin(job, "calculate")
    try:
        cfg = EngineConfig(use_live_market_feeds=True)
        engine = CBAMCalculationEngine(repo, config=cfg)
        run = engine.run()
        if not run.facility_reports:
            raise RuntimeError("calc engine produced zero facility reports")
        fr = run.facility_reports[0]
        product = fr.products[0] if fr.products else None
        for warning in fr.missing_data_warnings:
            _emit(job, f"warning: {warning}")
        if fr.total_emissions_tco2e <= 0:
            # A plant with output cannot have zero emissions: this means the
            # inputs are missing, so do not publish it as a successful report.
            raise RuntimeError(
                "calc engine produced 0 tCO2e for "
                f"{sum(p.output_tonnes for p in fr.products):,.0f} t of output in {fr.quarter}: "
                + ("; ".join(fr.missing_data_warnings) or "no activity data")
            )
        job.calc_summary = {
            "calc_run_id": run.run_id,
            "facility_id": fr.facility_id,
            "quarter": fr.quarter,
            "total_emissions_tco2e": fr.total_emissions_tco2e,
            "projected_cbam_cost_eur": fr.projected_cbam_cost_eur,
            "product_cn": product.product_cn_code if product else None,
            "total_see": product.total_see_tco2_per_t if product else None,
            "adjusted_see": product.adjusted_see_tco2_per_t if product else None,
            "uncertainty_pct": product.overall_uncertainty_pct if product else None,
            "share_estimated": product.share_of_estimated_emissions if product else None,
        }
        _succeed(job, s, f"{int(fr.total_emissions_tco2e):,} tCO2e total")
    except Exception as e:
        _fail(job, s, str(e))
        job.state = "failed"; job.error = str(e); job.finished_at = _now()
        return

    # 6. Render reports (XML + CSV + JSON)
    s = _begin(job, "render_reports")
    try:
        out_dir = Path("data/reports")
        paths = write_all(run, out_dir)
        job.artefacts = {k: str(v) for k, v in paths.items()}
        job.artefacts["calc_run_id"] = run.run_id
        _succeed(job, s, f"3 artefacts in {out_dir}/")
    except Exception as e:
        _fail(job, s, str(e))
        job.state = "failed"; job.error = str(e); job.finished_at = _now()
        return

    job.state = "succeeded"
    job.finished_at = _now()
    _emit(job, "✓✓✓ pipeline complete")


def _emit_demo_manual_supplements(
    job: JobState, orch: IngestionOrchestrator, repo: Repository, profile,
) -> str:
    """Add facility / meter / process / supplier / OCR rows for the demo.

    ERPNext has no meter or smelter data, so these values are SYNTHETIC. They are
    derived from the seeded production and BOMs for the quarter the calc engine
    will report on, because rows outside that quarter are ignored by the engine.
    Returns a one-line summary for the step detail.
    """
    runs = [r for r in repo.fetch_payloads("production_runs")
            if r.get("facility_id") == profile.facility_code]
    if not runs:
        raise RuntimeError(f"no production runs pulled for {profile.facility_code}")
    latest = max(date.fromisoformat(str(r["run_started_at"])[:10]) for r in runs)
    q_start, q_end = quarter_bounds(quarter_of(latest))

    output_by_item: dict[str, float] = defaultdict(float)
    for r in runs:
        if q_start <= date.fromisoformat(str(r["run_started_at"])[:10]) <= q_end:
            output_by_item[r.get("product_name", "")] += float(r.get("output_tonnes", 0))
    total_output_t = sum(output_by_item.values())

    def bom_input(item_code: str) -> float:
        return sum(
            output_by_item.get(p.item_code, 0.0) * line.qty_per_tonne_output
            for p in profile.products for line in p.bom if line.input_item == item_code
        )

    qs, qe = date(date.today().year, 1, 1), date(date.today().year, 12, 31)
    orch.run_manual("facility", [{
        "legal_entity_name": profile.legal_name,
        "company_registration_number": f"{profile.country}-DEMO-001",
        "plant_operating_name": profile.plant_name,
        "physical_address": "Demo address",
        "country": profile.country, "sector": profile.sector,
        "eu_cbam_declarant_name": "EU Importer GmbH",
        "cn_codes": [profile.products[0].item_code] if profile.products else [],
        "reporting_period_start": qs, "reporting_period_end": qe,
        "design_capacity_t_per_year": int(sum(p.monthly_output_tonnes_mean * 12 for p in profile.products)),
        "functional_currency": profile.currency,
        "eori": profile.eori,
        "un_locode": profile.un_locode,
        "cbam_installation_id": profile.cbam_installation_id,
    }])
    orch.run_sensor([{
        "facility_id": profile.facility_code,
        "period_start": q_start,
        "period_end": q_end,
        "meter_id": "MTR-DEMO-001",
        "meter_type": "electricity_subprocess",
        "cost_centre": profile.cost_centres[0] if profile.cost_centres else "site_total",
        "quantity": round(total_output_t * profile.electricity_kwh_per_tonne, 1), "unit": "kWh",
        "quality_flag": "ok",
    }])

    if profile.sector == "aluminium":
        orch.run_manual("aluminium_process_monthly", [{
            "facility_id": profile.facility_code,
            "period_start": q_start,
            "period_end": q_end,
            "alumina_consumed_tonnes": round(bom_input("ALUMINA-SG"), 3),
            "anode_consumption_tonnes": round(bom_input("ANODE-PREBAKE"), 3),
            "primary_al_output_tonnes": round(total_output_t, 3),
        }])
    elif profile.sector == "fertiliser":
        orch.run_manual("fertiliser_process_monthly", [{
            "facility_id": profile.facility_code,
            "period_start": q_start,
            "period_end": q_end,
            "feedstock_natural_gas_nm3": round(bom_input("NAT-GAS-FS"), 1),
            "ammonia_production_tonnes": round(output_by_item.get("AMMONIA-ANH", 0.0), 3),
            "urea_production_tonnes": round(output_by_item.get("UREA-PRILLED", 0.0), 3),
            "nitric_acid_production_tonnes": round(output_by_item.get("HNO3-58", 0.0), 3),
        }])

    # Supplier declaration for the largest real PO in the quarter. It cites the
    # PO number, so the calc engine replaces that row instead of adding tonnage.
    pos = [p for p in repo.fetch_payloads("precursor_purchases")
           if p.get("facility_id") == profile.facility_code and p.get("source") == "ERP"
           and q_start <= date.fromisoformat(str(p["purchase_date"])[:10]) <= q_end
           and cbam_default(p.get("precursor_cn_code") or "", p.get("supplier_country"), q_start.year)]
    if pos:
        po = max(pos, key=lambda p: float(p.get("quantity_tonnes", 0)))
        orch.run_supplier([{
            "facility_id": profile.facility_code,
            "po_number": po["po_number"],
            "precursor_name": po["precursor_name"],
            "precursor_cn_code": po["precursor_cn_code"],
            "quantity_tonnes": po["quantity_tonnes"],
            "supplier_name": po["supplier_name"],
            "supplier_country": po.get("supplier_country") or "??",
            # Demo: declared value slightly under the official default (before mark-up).
            "embedded_emissions_tco2_per_t": round(cbam_default(
                po["precursor_cn_code"], po.get("supplier_country"), q_start.year)["base"] * 0.95, 3),
            "ee_method": "actual",
            "purchase_date": po["purchase_date"],
        }])

    ocr_note = "OCR not run"
    sample = Path("data/samples/sample_electricity_invoice.png")
    if sample.exists():
        try:
            orch.run_ocr([sample], facility_id=profile.facility_code)
            ocr_note = "OCR added"
        except Exception as e:
            # OCR is optional (needs a local Tesseract install); keep the run going.
            ocr_note = "OCR skipped"
            _emit(job, f"OCR skipped: {str(e).splitlines()[0]}")
    return f"facility + meter + process + supplier added (synthetic demo values); {ocr_note}"
