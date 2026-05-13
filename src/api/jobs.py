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
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.calculation import CBAMCalculationEngine, EngineConfig, write_all
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
            _succeed(job, s, f"{report.work_orders} WOs + {report.purchase_orders} POs + {report.sales_invoices} SInv")
    except Exception as e:
        _fail(job, s, str(e))
        job.state = "failed"; job.error = str(e); job.finished_at = _now()
        return

    # 3. Pull canonical streams
    s = _begin(job, "pull_erp")
    try:
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
        _emit_demo_manual_supplements(orch, profile)
        _succeed(job, s, "facility + sensor + supplier + OCR added")
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


def _emit_demo_manual_supplements(orch: IngestionOrchestrator, profile) -> None:
    """One row each of facility / sensor / supplier / OCR so the audit view
    has all source types represented."""
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
        "period_start": date(date.today().year, max(1, date.today().month - 1), 1),
        "period_end": date.today(),
        "meter_id": "MTR-DEMO-001",
        "meter_type": "electricity_subprocess",
        "cost_centre": profile.cost_centres[0] if profile.cost_centres else "site_total",
        "quantity": 10_000_000, "unit": "kWh",
        "quality_flag": "ok",
    }])
    orch.run_supplier([{
        "facility_id": profile.facility_code,
        "po_number": "PO-DEMO-001",
        "precursor_name": profile.products[0].bom[0].input_item if profile.products and profile.products[0].bom else "alumina",
        "precursor_cn_code": "28182000",
        "quantity_tonnes": 25_000,
        "supplier_name": profile.suppliers[0].supplier_name if profile.suppliers else "Demo supplier",
        "supplier_country": profile.suppliers[0].country if profile.suppliers else "BR",
        "embedded_emissions_tco2_per_t": 1.05,
        "ee_method": "actual",
        "purchase_date": date.today(),
    }])
    sample = Path("data/samples/sample_electricity_invoice.png")
    if sample.exists():
        orch.run_ocr([sample], facility_id=profile.facility_code)
