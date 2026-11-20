"""Regression tests for the "run succeeds with 0 tCO2e" failure.

Covers: ERP item codes reaching the emissions tables, supplier declarations not
double-counting a PO, reruns replacing rows, and zero-emission runs failing.
"""
from datetime import date

import pytest

from src.api import jobs
from src.calculation.aggregation import aggregate_by_quarter
from src.core.models import PrecursorPurchase, ProductionRun
from src.ingestion.erp.erp_ingestor import _map_purchase_order
from src.ingestion.erp.erpnext_runner import _map_purchase_order_item
from src.seeding import get_profile


def _po_row(item_code: str, cn: str, qty: float = 100.0, uom: str = "tonnes") -> dict:
    return _map_purchase_order_item({
        "parent": "PO-1", "item_code": item_code, "qty": qty, "uom": uom, "rate": 1,
        "transaction_date": "2026-08-01", "schedule_date": "2026-08-20",
        "custom_facility_code": "F1", "custom_cn_code": cn,
        "custom_supplier_name": "S", "custom_supplier_country": "BR",
    })


@pytest.mark.parametrize("profile_key", ["mozal_aluminium", "ocp_fertiliser"])
def test_every_purchased_bom_input_maps_to_an_emissions_row(profile_key):
    """Item codes the seeder buys must not be dropped by the PO mapper."""
    profile = get_profile(profile_key)
    bought = {i for s in profile.suppliers for i in s.sells_items}
    bom_inputs = {ln.input_item for p in profile.products for ln in p.bom}
    # NAT-GAS-FS is feedstock, counted through the fertiliser process record.
    for item_code in (bought & bom_inputs) - {"NAT-GAS-FS"}:
        item = next(i for i in profile.items if i.item_code == item_code)
        rows = _map_purchase_order(_po_row(item_code, item.cn_code, uom=item.uom), "ref")
        assert len(rows) == 1, f"{item_code} produced no emissions row"


def test_alumina_po_becomes_precursor_purchase():
    rows = _map_purchase_order(_po_row("ALUMINA-SG", "28182000", qty=250), "ref")
    assert isinstance(rows[0], PrecursorPurchase)
    assert rows[0].quantity_tonnes == 250
    assert rows[0].precursor_cn_code == "28182000"


def _production(start: str = "2026-08-02") -> dict:
    return {"facility_id": "F1", "product_cn_code": "76011000", "output_tonnes": 100.0,
            "eu_export_tonnes": 50.0, "run_started_at": start}


def _precursor(po: str, source: str, qty: float = 10.0) -> dict:
    return {"facility_id": "F1", "po_number": po, "source": source, "quantity_tonnes": qty,
            "purchase_date": "2026-08-05", "precursor_cn_code": "28182000"}


def test_supplier_declaration_replaces_the_po_it_cites():
    buckets = aggregate_by_quarter(
        "F1", "2026-Q3", [_production()], [],
        [_precursor("PO-1", "ERP"), _precursor("PO-1", "SUPPLIER"), _precursor("PO-2", "ERP")],
        [], [], [], [], [],
    )
    rows = buckets["76011000"].precursors
    assert sorted((r["po_number"], r["source"]) for r in rows) == [
        ("PO-1", "SUPPLIER"), ("PO-2", "ERP"),
    ]


def test_clear_facility_removes_only_that_facility(repo):
    def run(facility: str) -> ProductionRun:
        return ProductionRun(
            source="ERP", facility_id=facility, sector="aluminium", product_name="X",
            product_cn_code="76011000", batch_run_id="B", output_tonnes=1,
            eu_export_tonnes=0, domestic_sales_tonnes=1,
            run_started_at="2026-08-01T00:00:00", run_ended_at="2026-08-01T01:00:00",
        )
    repo.save_many([run("F1"), run("F2"), run("UNASSIGNED")])
    assert repo.clear_facility("F1") == 2
    assert [r["facility_id"] for r in repo.fetch_payloads("production_runs")] == ["F2"]


def _run_pipeline_with_engine_total(monkeypatch, repo, total: float):
    """Drive _run_pipeline with ERPNext stubbed, returning the finished job."""
    class FakeClient:
        def __init__(self, creds): ...
        def ping(self): return True
        def get_count(self, *a, **k): return 1

    class FakeOrch:
        class report:
            results = []
        def __init__(self, repository): ...
        def run_erpnext_direct(self, creds): ...

    class Report:
        total_emissions_tco2e = total
        projected_cbam_cost_eur = 0.0
        facility_id, quarter = "MOZAL-MZ-01", "2026-Q3"
        products = []
        missing_data_warnings = ["No electricity or steam data"]

    class FakeRun:
        run_id = "r"
        facility_reports = [Report]

    class FakeEngine:
        def __init__(self, repo, config=None): ...
        def run(self): return FakeRun

    monkeypatch.setattr(jobs, "ERPNextClient", FakeClient)
    monkeypatch.setattr(jobs, "IngestionOrchestrator", FakeOrch)
    monkeypatch.setattr(jobs, "Repository", lambda: repo)
    monkeypatch.setattr(jobs, "CBAMCalculationEngine", FakeEngine)
    monkeypatch.setattr(jobs, "_emit_demo_manual_supplements", lambda *a: "ok")
    monkeypatch.setattr(jobs, "write_all", lambda run, out: {})

    job = jobs.JobState(
        run_id="j", profile_key="mozal_aluminium", base_url="http://x", started_at="now",
        steps=[jobs.StepStatus(name=n) for n in jobs._PIPELINE_STEPS],
    )
    jobs._run_pipeline(job, "k", "s", True, True)
    return job


def test_zero_emission_run_fails_instead_of_succeeding(monkeypatch, repo):
    job = _run_pipeline_with_engine_total(monkeypatch, repo, 0.0)
    assert job.state == "failed"
    assert "0 tCO2e" in job.error and "No electricity" in job.error
    assert jobs._step(job, "render_reports").state == "pending"


def test_nonzero_run_succeeds_and_logs_warnings(monkeypatch, repo):
    job = _run_pipeline_with_engine_total(monkeypatch, repo, 5.0)
    assert job.state == "succeeded"
    assert any("No electricity" in line for line in job.log_lines)


def test_demo_supplements_land_in_the_reported_quarter(repo, monkeypatch, tmp_path):
    """Meter, process and supplier rows must be dated inside the production quarter."""
    from src.ingestion.orchestrator import IngestionOrchestrator

    monkeypatch.chdir(tmp_path)  # no sample invoice here, so OCR is not attempted
    profile = get_profile("mozal_aluminium")
    repo.save_many([
        ProductionRun(
            source="ERP", facility_id=profile.facility_code, sector="aluminium",
            product_name="AL-INGOT-P1020", product_cn_code="76011000", batch_run_id="B",
            output_tonnes=1000, eu_export_tonnes=600, domestic_sales_tonnes=400,
            run_started_at="2026-08-01T00:00:00", run_ended_at="2026-08-01T10:00:00",
        ),
        PrecursorPurchase(
            source="ERP", facility_id=profile.facility_code, po_number="PO-9",
            # unwrought Al alloy: a CBAM good, so it gets a demo supplier declaration
            precursor_name="al_alloy_ingot", precursor_cn_code="76012000",
            quantity_tonnes=1925, supplier_name="Alunorte Refinery",
            supplier_country="BR", purchase_date=date(2026, 8, 3),
        ),
    ])
    job = jobs.JobState(run_id="j", profile_key=profile.key, base_url="x", started_at="now")
    note = jobs._emit_demo_manual_supplements(
        job, IngestionOrchestrator(repository=repo), repo, profile)
    assert "synthetic" in note

    energy = repo.fetch_payloads("energy_consumption")
    assert [(e["period_start"], e["period_end"]) for e in energy] == [("2026-07-01", "2026-09-30")]
    assert energy[0]["quantity"] == pytest.approx(1000 * profile.electricity_kwh_per_tonne)

    process = repo.fetch_payloads("aluminium_process")
    assert process[0]["primary_al_output_tonnes"] == pytest.approx(1000)
    assert process[0]["anode_consumption_tonnes"] == pytest.approx(430)

    supplier = [p for p in repo.fetch_payloads("precursor_purchases") if p["source"] == "SUPPLIER"]
    assert [p["po_number"] for p in supplier] == ["PO-9"]
    assert supplier[0]["quantity_tonnes"] == pytest.approx(1925)
