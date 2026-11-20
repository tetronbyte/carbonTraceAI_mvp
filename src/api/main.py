"""FastAPI app — the HTTP surface the Next.js frontend talks to.

  uvicorn src.api.main:app --reload --port 8000

Endpoints
─────────
  GET  /api/profiles                       factory profiles available for selection
  GET  /api/health                         server + ERPNext reachability probe
  POST /api/runs                           start a pipeline run (returns run_id)
  GET  /api/runs                           list runs (newest first)
  GET  /api/runs/{run_id}                  run status + summary
  GET  /api/runs/{run_id}/dashboard        dashboard JSON (post-success only)
  GET  /api/runs/{run_id}/xml              CBAM XML download
  GET  /api/runs/{run_id}/csv              CBAM CSV download
  GET  /api/runs/{run_id}/audit            audit view payload (ingestion + provenance)
  GET  /api/runs/{run_id}/raw-ref          look up a `raw_ref` back to its JSONL line

Everything is CORS-open by default for the local Next.js dev server (3000).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from src.api import jobs
from src.calculation.market_feeds import market_provenance
from src.ingestion.erp.erpnext_client import ERPNextClient, ERPNextCredentials
from src.seeding import PROFILES
from src.storage.repository import Repository
from src.utils.logger import get_logger

log = get_logger(__name__)

app = FastAPI(title="carbonTraceAI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Request / response models
# ============================================================================

class FactoryProfileSummary(BaseModel):
    key: str
    facility_code: str
    sector: str
    legal_name: str
    plant_name: str
    country: str
    currency: str
    electricity_supplier: str
    grid_ef_kgco2_per_kwh: float
    products: list[dict]


class StartRunRequest(BaseModel):
    profile_key: str = Field(examples=["mozal_aluminium"])
    base_url: str = Field(examples=["http://localhost:8080"])
    api_key: str
    api_secret: str
    seed_if_empty: bool = True
    fast_demo: bool = True


# ============================================================================
# Health + profiles
# ============================================================================

@app.get("/api/health")
def health(base_url: Optional[str] = Query(None)) -> dict:
    erpnext_reachable: Optional[bool] = None
    if base_url:
        try:
            import requests as _req
            r = _req.get(base_url.rstrip("/"), timeout=5, allow_redirects=True)
            erpnext_reachable = r.status_code < 500
        except Exception:
            erpnext_reachable = False
    return {
        "status": "ok",
        "erpnext_reachable": erpnext_reachable,
        "market_feeds": market_provenance(),
    }


@app.get("/api/profiles", response_model=list[FactoryProfileSummary])
def list_profiles() -> list[FactoryProfileSummary]:
    return [
        FactoryProfileSummary(
            key=p.key,
            facility_code=p.facility_code,
            sector=p.sector,
            legal_name=p.legal_name,
            plant_name=p.plant_name,
            country=p.country,
            currency=p.currency,
            electricity_supplier=p.electricity_supplier,
            grid_ef_kgco2_per_kwh=p.grid_ef_kgco2_per_kwh,
            products=[
                {"item_code": prod.item_code,
                 "monthly_output_tonnes": prod.monthly_output_tonnes_mean,
                 "eu_export_share": prod.eu_export_share_mean}
                for prod in p.products
            ],
        )
        for p in PROFILES.values()
    ]


# ============================================================================
# Pipeline runs
# ============================================================================

@app.post("/api/runs")
def start_run(payload: StartRunRequest) -> dict:
    if payload.profile_key not in PROFILES:
        raise HTTPException(404, f"Unknown profile {payload.profile_key}")
    job = jobs.create_job(
        profile_key=payload.profile_key,
        base_url=payload.base_url,
        api_key=payload.api_key,
        api_secret=payload.api_secret,
        seed_if_empty=payload.seed_if_empty,
        fast_demo=payload.fast_demo,
    )
    return job.to_dict()


@app.get("/api/runs")
def list_runs() -> list[dict]:
    return [j.to_dict() for j in jobs.list_jobs()]


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> dict:
    job = jobs.get_job(run_id)
    if not job:
        raise HTTPException(404, f"Run {run_id} not found")
    return job.to_dict()


# ============================================================================
# Dashboard + reports (post-success artefacts)
# ============================================================================

@app.get("/api/runs/{run_id}/dashboard")
def get_dashboard(run_id: str) -> JSONResponse:
    job = jobs.get_job(run_id)
    if not job or job.state != "succeeded":
        raise HTTPException(404, "Run not complete yet")
    path = Path(job.artefacts.get("json", ""))
    if not path.exists():
        raise HTTPException(404, "Dashboard JSON missing")
    return JSONResponse(json.loads(path.read_text()))


@app.get("/api/runs/{run_id}/xml")
def download_xml(run_id: str) -> FileResponse:
    job = jobs.get_job(run_id)
    if not job or "xml" not in job.artefacts:
        raise HTTPException(404, "XML not available")
    return FileResponse(job.artefacts["xml"], media_type="application/xml",
                        filename=f"cbam_quarterly_{run_id}.xml")


@app.get("/api/runs/{run_id}/csv")
def download_csv(run_id: str) -> FileResponse:
    job = jobs.get_job(run_id)
    if not job or "csv" not in job.artefacts:
        raise HTTPException(404, "CSV not available")
    return FileResponse(job.artefacts["csv"], media_type="text/csv",
                        filename=f"cbam_quarterly_{run_id}.csv")


# ============================================================================
# Audit view — what the verifier sees
# ============================================================================

@app.get("/api/runs/{run_id}/audit")
def get_audit_view(run_id: str) -> dict:
    """The verifier perspective: ingestion event log, every emission line with
    EF tier + source citation, reconciliation residuals, estimation flags,
    raw_ref drill-down handles per row."""
    job = jobs.get_job(run_id)
    if not job:
        raise HTTPException(404, "Run not found")
    repo = Repository()

    # Ingestion event log
    events: list[dict] = []
    try:
        with repo.engine.connect() as db:
            from sqlalchemy import text
            rows = db.execute(text(
                "SELECT source, stream, record_count, ok_count, error_count, "
                "       started_at, finished_at "
                "FROM ingestion_events ORDER BY started_at DESC LIMIT 200"
            )).mappings().all()
            events = [dict(r) for r in rows]
    except Exception as e:
        log.warning("ingestion_events fetch failed: %s", e)

    # Dashboard JSON contains every emission line with provenance.
    dashboard = {}
    if job.state == "succeeded":
        try:
            dashboard = json.loads(Path(job.artefacts["json"]).read_text())
        except Exception:
            pass

    # Table volumes — proves the ingestion depth.
    table_volumes: dict[str, int] = {}
    for table in (
        "production_runs", "energy_consumption", "precursor_purchases",
        "facilities", "aluminium_process", "fertiliser_process",
        "invoice_documents", "monitoring_meta", "stock_movements",
        "gl_entries", "outbound_shipments", "fugitive_emissions",
        "recs_certificates", "carbon_price_paid",
    ):
        try:
            table_volumes[table] = len(repo.fetch_payloads(table))
        except Exception:
            table_volumes[table] = 0

    return {
        "run": job.to_dict(),
        "ingestion_events": events,
        "table_volumes": table_volumes,
        "dashboard": dashboard,
        "market_feeds": market_provenance(),
    }


@app.get("/api/runs/{run_id}/raw-ref")
def lookup_raw_ref(run_id: str, ref: str = Query(...)) -> dict:
    """Resolve a `raw_ref` (e.g. `data/raw/erpnext/production_runs/...jsonl:42`)
    back to the JSONL line so the verifier can audit-trail any number."""
    try:
        path_part, line_no = ref.rsplit(":", 1)
        line_no = int(line_no)
    except ValueError:
        raise HTTPException(400, f"Invalid raw_ref: {ref}")
    path = Path(path_part)
    if not path.exists():
        raise HTTPException(404, f"Source JSONL not found: {path}")
    with path.open() as f:
        for i, line in enumerate(f, 1):
            if i == line_no:
                return {"raw_ref": ref, "payload": json.loads(line)}
    raise HTTPException(404, f"Line {line_no} not found in {path}")
