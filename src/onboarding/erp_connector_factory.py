"""ErpConnectorFactory — single dispatch point for "run a sync for this connection".

Routes:
  erpnext_direct  → ERPNextRunner (direct REST against the Frappe API)
  erpnext_airbyte → AirbyteProvisioner + ERPNext Airbyte source spec
  sap_* / oracle_* / etc. → AirbyteProvisioner with the registry's source-definition id

Whatever the path, the JSONL produced lands in `data/raw/<source>/<stream>/...`
and is consumed by the existing `ErpIngestor` mappers — the downstream
canonical store and calc engine do not know (and do not care) which path ran.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from src.core.base import IngestionResult
from src.ingestion.erp.erp_ingestor import ErpIngestor
from src.ingestion.erp.erpnext_client import ERPNextClient, ERPNextCredentials
from src.ingestion.erp.erpnext_runner import ERPNextRunner
from src.storage.repository import Repository
from src.utils.logger import get_logger

from .airbyte_provisioner import (
    AirbyteProvisioner,
    ProvisioningError,
    mark_connection_state,
)
from .client_connection import ClientConnection, ConnectionRepository, ConnectionStatus
from .connector_registry import ConnectorSpec, get_connector
from .credential_vault import CredentialVault

log = get_logger(__name__)


@dataclass
class SyncOutcome:
    connection: ClientConnection
    ingestion_results: list[IngestionResult] = field(default_factory=list)
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and all(r.ok for r in self.ingestion_results)

    def summary(self) -> str:
        head = (
            f"[{self.connection.connector_key}] facility={self.connection.facility_id} "
            f"status={self.connection.status}"
        )
        if self.error:
            return f"{head}\n  ERROR: {self.error}"
        body = "\n".join(r.summary() for r in self.ingestion_results)
        return f"{head}\n{body}" if body else head


class ErpConnectorFactory:
    """Routes a saved ClientConnection to its actual ingestion path."""

    def __init__(
        self,
        repository: Repository,
        connections: ConnectionRepository,
        vault: CredentialVault,
        provisioner: AirbyteProvisioner | None = None,
    ) -> None:
        self.repository = repository
        self.connections = connections
        self.vault = vault
        self.provisioner = provisioner or AirbyteProvisioner()

    # ---- public API ----
    def sync(self, connection_id: str) -> SyncOutcome:
        conn = self.connections.get(connection_id)
        if not conn:
            raise KeyError(f"No client connection with id {connection_id!r}")
        spec = get_connector(conn.connector_key)
        log.info("Sync requested: %s (%s)", conn.id, spec.display_name)

        if spec.key == "erpnext_direct":
            return self._run_erpnext_direct(conn)
        if spec.key == "erpnext_airbyte":
            return self._run_erpnext_airbyte(conn, spec)
        return self._run_airbyte_generic(conn, spec)

    # ---- branches ------------------------------------------------------------
    def _run_erpnext_direct(self, conn: ClientConnection) -> SyncOutcome:
        creds_dict = conn.reveal_credentials(self.vault)
        creds = ERPNextCredentials(
            base_url=creds_dict["base_url"],
            api_key=creds_dict.get("api_key"),
            api_secret=creds_dict.get("api_secret"),
        )
        client = ERPNextClient(creds)
        if not client.ping():
            err = f"ERPNext unreachable at {creds.base_url}"
            mark_connection_state(conn, None, status=ConnectionStatus.ERRORED)
            self.connections.save(conn)
            return SyncOutcome(connection=conn, error=err)

        mark_connection_state(conn, None, status=ConnectionStatus.SYNCING)
        self.connections.save(conn)

        runner = ERPNextRunner(client)
        landings = runner.sync_all()
        first_dir = next(iter(landings.values())).parent.parent if landings else None
        conn.last_landing_dir = str(first_dir) if first_dir else None
        conn.last_sync_status = "completed_direct_rest"
        mark_connection_state(conn, None, status=ConnectionStatus.SYNCED)
        self.connections.save(conn)

        results = self._ingest_landings(landings)
        return SyncOutcome(connection=conn, ingestion_results=results)

    def _run_erpnext_airbyte(self, conn: ClientConnection, spec: ConnectorSpec) -> SyncOutcome:
        return self._run_airbyte_generic(conn, spec)

    def _run_airbyte_generic(self, conn: ClientConnection, spec: ConnectorSpec) -> SyncOutcome:
        try:
            if not conn.airbyte_connection_id:
                result = self.provisioner.provision(conn, self.vault)
                mark_connection_state(conn, result, status=ConnectionStatus.PROVISIONED)
                self.connections.save(conn)

            mark_connection_state(conn, None, status=ConnectionStatus.SYNCING)
            self.connections.save(conn)
            sync = self.provisioner.trigger_sync(conn.airbyte_connection_id)  # type: ignore[arg-type]
            mark_connection_state(conn, None, status=ConnectionStatus.SYNCED, sync=sync)
            self.connections.save(conn)

            landing_dir = Path(conn.last_landing_dir or "")
            stream_to_path = self._discover_landings(spec, landing_dir)
            results = self._ingest_landings(stream_to_path)
            return SyncOutcome(connection=conn, ingestion_results=results)

        except ProvisioningError as e:
            log.error("Provisioning failed: %s", e.message)
            mark_connection_state(conn, None, status=ConnectionStatus.AIRBYTE_UNAVAILABLE)
            self.connections.save(conn)
            return SyncOutcome(connection=conn, error=e.message)

    # ---- helpers -------------------------------------------------------------
    def _discover_landings(self, spec: ConnectorSpec, landing_dir: Path) -> dict[str, Path]:
        out: dict[str, Path] = {}
        for sm in spec.streams:
            stream_dir = landing_dir / sm.canonical_stream
            if not stream_dir.exists():
                continue
            jsonls = sorted(stream_dir.glob("*.jsonl"))
            if jsonls:
                out[sm.canonical_stream] = jsonls[-1]
        return out

    def _ingest_landings(self, stream_to_path: dict[str, Path]) -> list[IngestionResult]:
        results: list[IngestionResult] = []
        for stream, path in stream_to_path.items():
            ing = ErpIngestor(self.repository, stream=stream, landing_path=path)
            results.append(ing.run())
        return results
