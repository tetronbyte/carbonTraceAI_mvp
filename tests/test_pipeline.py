"""Smoke tests for the carbonTraceAI ingestion pipeline (post-ERPNext pivot)."""
from datetime import date
from unittest.mock import MagicMock

import pytest

from src.ingestion.erp.erp_ingestor import ErpIngestor
from src.ingestion.erp.erpnext_client import ERPNextClient, ERPNextCredentials
from src.ingestion.erp.erpnext_runner import ERPNextRunner
from src.ingestion.manual.manual_ingestor import (
    ManualIngestor, SensorIngestor, SupplierPortalIngestor,
)
from src.ingestion.ocr.invoice_parser import InvoiceParser


# =========================================================================
# ERPNext client / runner — mocked HTTP
# =========================================================================

def _fake_work_order(i: int) -> dict:
    return {
        "name": f"MFG-{i:04d}",
        "production_item": "AL-INGOT-P1020",
        "qty": 100, "produced_qty": 99,
        "planned_start_date": "2026-04-01 08:00:00",
        "actual_start_date": "2026-04-01 08:00:00",
        "actual_end_date":   "2026-04-01 22:00:00",
        "status": "Completed",
        "custom_facility_code": "MOZAL-MZ-01",
        "custom_sector": "aluminium",
        "custom_cn_code": "76011000",
        "custom_eu_export_share": 0.6,
        "custom_scrap_rate_pct": 1.2,
    }


def _fake_po_item(i: int) -> dict:
    return {
        "name": f"POL-{i:04d}", "parent": f"PO-{i:04d}",
        "item_code": "ALUMINA-SG",
        "qty": 250, "uom": "tonnes", "stock_uom": "tonnes",
        "rate": 320, "transaction_date": "2026-04-15",
        "schedule_date": "2026-05-01",
        "custom_facility_code": "MOZAL-MZ-01",
        "custom_cn_code": "28182000",
        "custom_supplier_name": "Alunorte Refinery",
        "custom_supplier_country": "BR",
    }


def test_erpnext_client_iter_all_paginates(monkeypatch):
    creds = ERPNextCredentials(base_url="http://erp.test", api_key="k", api_secret="s")
    client = ERPNextClient(creds)

    pages = [
        [_fake_work_order(i) for i in range(200)],  # full page
        [_fake_work_order(i) for i in range(200, 350)],  # partial → stop
    ]
    calls = {"n": 0}

    def fake_get_list(doctype, **kw):
        page = pages[calls["n"]] if calls["n"] < len(pages) else []
        calls["n"] += 1
        return page

    monkeypatch.setattr(client, "get_list", fake_get_list)
    rows = list(client.iter_all("Work Order", page_size=200))
    assert len(rows) == 350
    assert calls["n"] == 2


def test_erpnext_runner_writes_canonical_jsonl(monkeypatch, tmp_path):
    monkeypatch.setenv("CARBONTRACE_DATA_DIR", str(tmp_path))
    from importlib import reload
    import config.settings as cs; reload(cs)
    import src.utils.raw_landing as rl; reload(rl)
    import src.ingestion.erp.erpnext_runner as rn_mod; reload(rn_mod)
    from src.ingestion.erp.erpnext_runner import ERPNextRunner as ERPNextRunnerFresh

    client = MagicMock(spec=ERPNextClient)
    def iter_all(doctype, **_):
        if doctype == "Work Order":
            yield from (_fake_work_order(i) for i in range(5))
        elif doctype == "Purchase Order Item":
            yield from (_fake_po_item(i) for i in range(3))
        else:
            yield from ()
    client.iter_all.side_effect = iter_all

    runner = ERPNextRunnerFresh(client)
    landings = runner.sync_all()
    assert set(landings) == {"production_runs", "purchase_orders", "bill_of_materials", "invoices"}
    prod_lines = landings["production_runs"].read_text().strip().splitlines()
    po_lines = landings["purchase_orders"].read_text().strip().splitlines()
    assert len(prod_lines) == 5
    assert len(po_lines) == 3


def test_erp_ingestor_consumes_erpnext_landing(repo, monkeypatch, tmp_path):
    monkeypatch.setenv("CARBONTRACE_DATA_DIR", str(tmp_path))
    from importlib import reload
    import config.settings as cs; reload(cs)
    import src.utils.raw_landing as rl; reload(rl)
    import src.ingestion.erp.erpnext_runner as rn_mod; reload(rn_mod)
    from src.ingestion.erp.erpnext_runner import ERPNextRunner as ERPNextRunnerFresh

    client = MagicMock(spec=ERPNextClient)
    def iter_all(doctype, **_):
        if doctype == "Work Order":
            yield from (_fake_work_order(i) for i in range(7))
        else:
            yield from ()
    client.iter_all.side_effect = iter_all

    runner = ERPNextRunnerFresh(client)
    landings = runner.sync_all()

    ing = ErpIngestor(repo, stream="production_runs", landing_path=landings["production_runs"])
    result = ing.run()
    assert result.event.ok_count == 7
    rows = repo.fetch_payloads("production_runs")
    assert len(rows) == 7
    assert all(r["product_cn_code"] == "76011000" for r in rows)
    # EU export split — eu_export_share=0.6 → ~60% of output goes to EU
    assert rows[0]["eu_export_tonnes"] > 0
    assert rows[0]["domestic_sales_tonnes"] > 0
    assert rows[0]["eu_export_tonnes"] + rows[0]["domestic_sales_tonnes"] == pytest.approx(
        rows[0]["output_tonnes"], rel=1e-3,
    )


# =========================================================================
# Manual / Sensor / Supplier — unchanged plumbing
# =========================================================================

def test_manual_ingestor_facility(repo):
    ing = ManualIngestor(repo, form_id="facility", submissions=[{
        "legal_entity_name": "Mozal SA", "company_registration_number": "MZ-100",
        "plant_operating_name": "Mozal Smelter", "physical_address": "Beluluane",
        "country": "MZ", "sector": "aluminium",
        "reporting_period_start": date(2026, 1, 1),
        "reporting_period_end":   date(2026, 12, 31),
    }])
    res = ing.run()
    assert res.ok and res.event.ok_count == 1


def test_sensor_ingestor_manual(repo):
    ing = SensorIngestor(repo, submissions=[{
        "facility_id": "MOZAL-MZ-01",
        "period_start": date(2026, 4, 1), "period_end": date(2026, 4, 30),
        "meter_type": "electricity_grid", "quantity": 1000, "unit": "kWh",
    }])
    res = ing.run()
    assert res.ok


def test_supplier_portal(repo):
    ing = SupplierPortalIngestor(repo, submissions=[{
        "facility_id": "MOZAL-MZ-01",
        "precursor_name": "alumina", "precursor_cn_code": "28182000",
        "quantity_tonnes": 100, "supplier_name": "Alunorte Refinery",
        "supplier_country": "BR", "embedded_emissions_tco2_per_t": 1.05,
        "ee_method": "actual", "purchase_date": date(2026, 3, 15),
    }])
    res = ing.run()
    rows = repo.fetch_payloads("precursor_purchases")
    assert res.ok and rows[0]["source"] == "SUPPLIER"


# =========================================================================
# OCR invoice parser (unchanged)
# =========================================================================

def test_invoice_parser_extracts_basic_fields():
    text = (
        "EDM SA\nInvoice Number: INV-2026-00821\nInvoice Date: 2026-04-30\n"
        "Total consumption: 712,000 kWh\nTotal amount due: USD 12,000,000\n"
    )
    parsed = InvoiceParser().parse(text, ocr_confidence=0.85)
    assert parsed.category == "electricity"
    assert parsed.invoice_number == "INV-2026-00821"
    assert parsed.invoice_date == date(2026, 4, 30)
    assert parsed.quantity == 712000.0
    assert parsed.unit == "kWh"


# =========================================================================
# Connector registry + onboarding
# =========================================================================

def test_connector_registry_lists_erpnext_first():
    from src.onboarding import list_connectors
    specs = list_connectors()
    assert specs[0].vendor == "Frappe Technologies"
    keys = {s.key for s in specs}
    assert {"erpnext_direct", "erpnext_airbyte",
            "sap_s4hana_jdbc", "oracle_ebs", "ms_dynamics_365",
            "netsuite", "sage_x3", "odoo"} <= keys
    # No DataGen entry should remain.
    assert "datagen_simulated" not in keys


def test_credential_vault_roundtrip(tmp_path, monkeypatch):
    from cryptography.fernet import Fernet
    from src.onboarding import CredentialVault
    monkeypatch.setenv("CARBONTRACE_VAULT_KEY", Fernet.generate_key().decode())
    v = CredentialVault()
    secret = "ngrok-tunnel-supersecret-9!"
    token = v.encrypt({"api_key": "abc123", "api_secret": secret})
    assert secret not in token and "abc123" not in token
    assert v.decrypt(token) == {"api_key": "abc123", "api_secret": secret}


def test_client_connection_validates_required_creds(monkeypatch):
    from cryptography.fernet import Fernet
    from src.onboarding import ClientConnection, CredentialVault
    from src.core.exceptions import ValidationError
    monkeypatch.setenv("CARBONTRACE_VAULT_KEY", Fernet.generate_key().decode())
    vault = CredentialVault()
    with pytest.raises(ValidationError):
        ClientConnection.from_creds(
            facility_id="MOZAL-MZ-01",
            connector_key="erpnext_direct",
            creds={"base_url": "http://localhost:8080"},  # missing api_key / secret
            vault=vault,
        )


def test_factory_erpnext_direct_errors_when_unreachable(tmp_path, monkeypatch):
    """If ERPNext is offline, the factory surfaces the error — no fake fallback."""
    from cryptography.fernet import Fernet
    from src.onboarding import (
        ClientConnection, ConnectionRepository, CredentialVault, ErpConnectorFactory,
    )
    monkeypatch.setenv("CARBONTRACE_VAULT_KEY", Fernet.generate_key().decode())
    monkeypatch.setenv("CARBONTRACE_DB_URL", f"sqlite:///{tmp_path / 'fact.db'}")
    from importlib import reload
    import config.settings as cs; reload(cs)
    from src.storage.repository import Repository

    repo = Repository(db_url=cs.settings.db_url)
    connections = ConnectionRepository(db_url=cs.settings.db_url)
    vault = CredentialVault()

    conn = ClientConnection.from_creds(
        facility_id="MOZAL-MZ-01",
        connector_key="erpnext_direct",
        creds={"base_url": "http://localhost:1",  # nothing listens here
               "api_key": "k", "api_secret": "s"},
        vault=vault,
    )
    connections.save(conn)

    factory = ErpConnectorFactory(repository=repo, connections=connections, vault=vault)
    outcome = factory.sync(conn.id)
    assert outcome.error and "unreachable" in outcome.error.lower()
    assert outcome.connection.status in ("errored", "ERRORED")
