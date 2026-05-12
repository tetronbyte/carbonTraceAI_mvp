"""Registry of supported ERP connectors.

Each entry describes:
  - what credentials the connector needs (used to generate the onboarding form)
  - the Airbyte source-definition ID (so we can call /sources/create)
  - the streams the connector exposes and how each stream maps to the canonical
    canonical ErpIngestor stream name (production_runs / purchase_orders / ...)

Adding a new connector = adding one entry. No code changes elsewhere.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class CredentialField:
    name: str                # form field name
    label: str               # UI label
    secret: bool = False     # mask in UI; encrypt at rest
    required: bool = True
    help_text: Optional[str] = None
    placeholder: Optional[str] = None


@dataclass(frozen=True)
class StreamMapping:
    """Map a connector-specific stream to our canonical ERP stream name."""
    canonical_stream: str         # one of: production_runs, purchase_orders, invoices,
                                  #         energy_meter_readings, bill_of_materials
    connector_stream: str         # the name the connector actually exposes
    sql_query: Optional[str] = None  # optional override (for JDBC-style connectors)


@dataclass(frozen=True)
class ConnectorSpec:
    key: str                                       # registry key
    display_name: str                              # for UI dropdown
    vendor: str                                    # SAP, Oracle, ...
    airbyte_source_definition_id: Optional[str]    # None for the simulated path
    description: str
    credentials: list[CredentialField]
    streams: list[StreamMapping]
    is_simulated: bool = False
    docs_url: Optional[str] = None


# ---------------------------------------------------------------------------
# Connector definitions
# ---------------------------------------------------------------------------

# Canonical streams the ErpIngestor consumes.
_CANONICAL_STREAMS = (
    "production_runs",
    "purchase_orders",
    "invoices",
    "energy_meter_readings",
    "bill_of_materials",
)


def _generic_jdbc_streams() -> list[StreamMapping]:
    """Default stream layout when the source is queried via SQL — most ERPs
    expose data through views or staging tables. Tenants override per install."""
    return [
        StreamMapping(canonical_stream=cs, connector_stream=f"vw_carbontrace_{cs}")
        for cs in _CANONICAL_STREAMS
    ]


CONNECTOR_REGISTRY: dict[str, ConnectorSpec] = {
    # ---- ERPNext via direct REST (Frappe API) ----
    # Default demo path: works against any ERPNext instance — local Docker,
    # ngrok-tunnelled, or production — without needing an Airbyte deployment.
    "erpnext_direct": ConnectorSpec(
        key="erpnext_direct",
        display_name="ERPNext (direct REST)",
        vendor="Frappe Technologies",
        airbyte_source_definition_id=None,
        description="Pulls Work Orders, Purchase Orders, BOMs, and Purchase Invoices "
                    "from an ERPNext instance via the Frappe REST API. Use this path "
                    "for local Docker demos, ngrok-tunnelled sandboxes, or any deployment "
                    "where you don't (yet) have an Airbyte cluster.",
        credentials=[
            CredentialField("base_url",   "ERPNext base URL",
                            placeholder="http://localhost:8080",
                            help_text="Use the ngrok URL for cloud Airbyte / remote pitches."),
            CredentialField("api_key",    "API key",    secret=True),
            CredentialField("api_secret", "API secret", secret=True),
        ],
        streams=[
            StreamMapping("production_runs",   "Work Order"),
            StreamMapping("purchase_orders",   "Purchase Order Item"),
            StreamMapping("bill_of_materials", "BOM Item"),
            StreamMapping("invoices",          "Purchase Invoice"),
        ],
        docs_url="https://frappeframework.com/docs/user/en/api/rest",
    ),

    # ---- ERPNext via Airbyte (official Airbyte ERPNext source) ----
    # Same ERPNext data, but ingestion goes Source → Airbyte → file destination → us.
    # Use for production / multi-tenant scale. Auth is the same API key/secret pair.
    "erpnext_airbyte": ConnectorSpec(
        key="erpnext_airbyte",
        display_name="ERPNext (via Airbyte)",
        vendor="Frappe Technologies",
        airbyte_source_definition_id="ec8d3e62-5b96-44f3-bdde-7d2e6d3c4ce4",
        description="ERPNext as an Airbyte source — recommended once an Airbyte "
                    "deployment is available. The same auth as erpnext_direct.",
        credentials=[
            CredentialField("base_url",   "ERPNext base URL",
                            placeholder="https://erp.client.com"),
            CredentialField("api_key",    "API key",    secret=True),
            CredentialField("api_secret", "API secret", secret=True),
        ],
        streams=[
            StreamMapping("production_runs",   "Work Order"),
            StreamMapping("purchase_orders",   "Purchase Order Item"),
            StreamMapping("bill_of_materials", "BOM Item"),
            StreamMapping("invoices",          "Purchase Invoice"),
        ],
        docs_url="https://docs.airbyte.com/integrations/sources/erpnext",
    ),

    # ---- SAP S/4HANA via JDBC (HANA SQL endpoint) ----
    "sap_s4hana_jdbc": ConnectorSpec(
        key="sap_s4hana_jdbc",
        display_name="SAP S/4HANA (HANA JDBC)",
        vendor="SAP",
        airbyte_source_definition_id="b5ea17b1-f170-46dc-bc31-cc744ca984c1",  # SAP HANA spec id
        description="Pulls production, BOM, PO, invoice, and meter views from SAP HANA. "
                    "Requires a read-only DB user and a set of pre-built views named vw_carbontrace_*.",
        credentials=[
            CredentialField("host",     "HANA host",   placeholder="hana.client.local"),
            CredentialField("port",     "Port",        placeholder="30015"),
            CredentialField("database", "Tenant DB",   placeholder="HXE"),
            CredentialField("schema",   "Schema",      placeholder="CARBONTRACE"),
            CredentialField("username", "Service user", placeholder="CT_READER"),
            CredentialField("password", "Password",    secret=True),
            CredentialField("client_id","SAP client",  required=False, placeholder="100"),
        ],
        streams=_generic_jdbc_streams(),
        docs_url="https://docs.airbyte.com/integrations/sources/sap-hana",
    ),

    # ---- Oracle EBS / Oracle Cloud (database) ----
    "oracle_ebs": ConnectorSpec(
        key="oracle_ebs",
        display_name="Oracle E-Business Suite (Oracle DB)",
        vendor="Oracle",
        airbyte_source_definition_id="b39a7370-74c3-45a6-ac3a-380d48520a83",  # Oracle DB spec id
        description="Pulls views/stage tables from an Oracle EBS instance.",
        credentials=[
            CredentialField("host",     "Host"),
            CredentialField("port",     "Port", placeholder="1521"),
            CredentialField("sid",      "SID", required=False),
            CredentialField("service_name", "Service name", required=False),
            CredentialField("schema",   "Schema", placeholder="CARBONTRACE"),
            CredentialField("username", "Username"),
            CredentialField("password", "Password", secret=True),
        ],
        streams=_generic_jdbc_streams(),
        docs_url="https://docs.airbyte.com/integrations/sources/oracle",
    ),

    # ---- Microsoft Dynamics 365 F&O (REST/OData) ----
    "ms_dynamics_365": ConnectorSpec(
        key="ms_dynamics_365",
        display_name="Microsoft Dynamics 365 F&O",
        vendor="Microsoft",
        airbyte_source_definition_id="f1e4c7e6-3a7a-4d11-a0c2-c9b0a8f0d57a",  # placeholder, actual id provisioned per workspace
        description="OData-based ingestion for Dynamics 365 Finance & Operations.",
        credentials=[
            CredentialField("base_url",      "OData base URL", placeholder="https://client.dynamics.com/data"),
            CredentialField("tenant_id",     "Azure tenant ID"),
            CredentialField("client_id",     "Application (client) ID"),
            CredentialField("client_secret", "Client secret", secret=True),
            CredentialField("company",       "Company code"),
        ],
        streams=[
            StreamMapping("production_runs",       "ProductionOrders"),
            StreamMapping("purchase_orders",       "PurchaseOrderLines"),
            StreamMapping("invoices",              "VendorInvoiceLines"),
            StreamMapping("energy_meter_readings", "AssetMeterReadings"),
            StreamMapping("bill_of_materials",     "BillOfMaterialsLines"),
        ],
        docs_url="https://docs.airbyte.com/integrations/sources/microsoft-dataverse",
    ),

    # ---- NetSuite (SuiteAnalytics Connect / OData) ----
    "netsuite": ConnectorSpec(
        key="netsuite",
        display_name="Oracle NetSuite",
        vendor="Oracle",
        airbyte_source_definition_id="0b50f7a8-2ee1-4f4e-b9a5-5fa5c0b7e99c",  # placeholder
        description="NetSuite via SuiteAnalytics. Requires Token-Based Authentication.",
        credentials=[
            CredentialField("account_id",        "NetSuite account ID"),
            CredentialField("consumer_key",      "Consumer key", secret=True),
            CredentialField("consumer_secret",   "Consumer secret", secret=True),
            CredentialField("token_id",          "Token ID", secret=True),
            CredentialField("token_secret",      "Token secret", secret=True),
        ],
        streams=[
            StreamMapping("production_runs",       "WorkOrder"),
            StreamMapping("purchase_orders",       "PurchaseOrder"),
            StreamMapping("invoices",              "VendorBill"),
            StreamMapping("energy_meter_readings", "CustomRecord_meter_reading"),
            StreamMapping("bill_of_materials",     "ItemRevision"),
        ],
        docs_url="https://docs.airbyte.com/integrations/sources/netsuite",
    ),

    # ---- Sage X3 / Sage 300 (REST or DB) ----
    "sage_x3": ConnectorSpec(
        key="sage_x3",
        display_name="Sage X3",
        vendor="Sage",
        airbyte_source_definition_id=None,  # custom REST source — provisioned per tenant
        description="Sage X3 via REST API (with optional DB fallback). Often used by African mid-caps.",
        credentials=[
            CredentialField("base_url",   "Sage X3 base URL", placeholder="https://x3.client.local/api"),
            CredentialField("username",   "Username"),
            CredentialField("password",   "Password", secret=True),
            CredentialField("company",    "Company code"),
        ],
        streams=[
            StreamMapping("production_runs",       "MFGOPS"),
            StreamMapping("purchase_orders",       "PORDER"),
            StreamMapping("invoices",              "PINVOIC"),
            StreamMapping("energy_meter_readings", "ZMETER"),
            StreamMapping("bill_of_materials",     "BOMD"),
        ],
    ),

    # ---- Odoo (often used by smaller plants) ----
    "odoo": ConnectorSpec(
        key="odoo",
        display_name="Odoo",
        vendor="Odoo SA",
        airbyte_source_definition_id="3826e85f-1696-4b6c-90f8-d02e3a23d5cf",  # placeholder
        description="Odoo via XML-RPC / JSON-RPC. Common for African SMEs.",
        credentials=[
            CredentialField("url",      "Odoo URL", placeholder="https://erp.client.com"),
            CredentialField("database", "Database name"),
            CredentialField("username", "Username"),
            CredentialField("password", "Password / API key", secret=True),
        ],
        streams=[
            StreamMapping("production_runs",       "mrp.production"),
            StreamMapping("purchase_orders",       "purchase.order.line"),
            StreamMapping("invoices",              "account.move.line"),
            StreamMapping("energy_meter_readings", "x_meter_reading"),
            StreamMapping("bill_of_materials",     "mrp.bom.line"),
        ],
        docs_url="https://docs.airbyte.com/integrations/sources/odoo",
    ),
}


_VENDOR_ORDER = ("Frappe Technologies", "SAP", "Oracle", "Microsoft", "Sage", "Odoo SA")


def list_connectors() -> list[ConnectorSpec]:
    """Sorted list — UIs render this directly. ERPNext (the demo target) first."""
    def _key(s: ConnectorSpec) -> tuple:
        try:
            idx = _VENDOR_ORDER.index(s.vendor)
        except ValueError:
            idx = len(_VENDOR_ORDER)
        return (idx, s.display_name)
    return sorted(CONNECTOR_REGISTRY.values(), key=_key)


def get_connector(key: str) -> ConnectorSpec:
    if key not in CONNECTOR_REGISTRY:
        raise KeyError(f"Unknown connector {key!r}. Known: {list(CONNECTOR_REGISTRY)}")
    return CONNECTOR_REGISTRY[key]
