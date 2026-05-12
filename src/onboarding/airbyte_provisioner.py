"""Idempotent Airbyte provisioning.

For each ClientConnection, ensures:
  1. an Airbyte Source exists (configured with the client's creds + connector spec)
  2. a File destination writes JSONL to `data/raw/airbyte/<conn-id>/<stream>/...`
  3. a Connection ties source → destination with the canonical stream selection

The provisioner is a thin wrapper over `AirbyteClient`. If Airbyte is
unreachable (no live deployment, network error, auth failure), it raises
`ProvisioningError` — the factory catches that and falls back gracefully.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import requests

from config.settings import settings
from src.core.exceptions import CarbonTraceError
from src.ingestion.erp.airbyte_client import AirbyteClient, AirbyteSyncResult
from src.utils.logger import get_logger

from .client_connection import ClientConnection, ConnectionStatus
from .connector_registry import ConnectorSpec, get_connector
from .credential_vault import CredentialVault

log = get_logger(__name__)


class ProvisioningError(CarbonTraceError):
    code = "provisioning_error"


@dataclass
class ProvisioningResult:
    source_id: Optional[str]
    destination_id: Optional[str]
    connection_id: Optional[str]
    landing_dir: Path


class AirbyteProvisioner:
    def __init__(
        self,
        client: AirbyteClient | None = None,
        workspace_id: str | None = None,
    ) -> None:
        self.client = client or AirbyteClient()
        self.workspace_id = workspace_id or "default"

    # ---- public ----
    def is_reachable(self) -> bool:
        """Quick health check — used by the factory to decide simulation fallback."""
        try:
            url = f"{self.client.api_url}/health"
            resp = requests.get(url, auth=self.client.auth, timeout=3)
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def provision(
        self,
        connection: ClientConnection,
        vault: CredentialVault,
    ) -> ProvisioningResult:
        spec = get_connector(connection.connector_key)
        if spec.is_simulated:
            raise ProvisioningError(
                "Simulated connector does not need provisioning — call ErpConnectorFactory directly.",
                connector_key=connection.connector_key,
            )
        if not spec.airbyte_source_definition_id:
            raise ProvisioningError(
                f"Connector {spec.key!r} has no Airbyte source-definition mapping yet.",
                connector_key=spec.key,
            )
        if not self.is_reachable():
            raise ProvisioningError(
                "Airbyte is not reachable. Connection saved but cannot be synced.",
                airbyte_url=self.client.api_url,
            )

        creds = connection.reveal_credentials(vault)
        landing_dir = settings.raw_dir / "airbyte" / connection.id
        landing_dir.mkdir(parents=True, exist_ok=True)

        source_id = self._ensure_source(spec, creds, connection.id)
        destination_id = self._ensure_file_destination(landing_dir, connection.id)
        connection_id = self._ensure_connection(spec, source_id, destination_id, connection.id)

        return ProvisioningResult(
            source_id=source_id,
            destination_id=destination_id,
            connection_id=connection_id,
            landing_dir=landing_dir,
        )

    def trigger_sync(self, airbyte_connection_id: str) -> AirbyteSyncResult:
        return self.client.trigger_sync(airbyte_connection_id)

    # ---- internals (Airbyte API calls — kept thin) ----
    def _ensure_source(self, spec: ConnectorSpec, creds: dict[str, Any], conn_id: str) -> str:
        body = {
            "workspaceId": self.workspace_id,
            "name": f"carbontrace-{spec.key}-{conn_id[:8]}",
            "sourceDefinitionId": spec.airbyte_source_definition_id,
            "connectionConfiguration": creds,
        }
        log.info("Airbyte: creating source for %s", spec.key)
        out = self.client._post("/sources/create", body)  # noqa: SLF001
        return out["sourceId"]

    def _ensure_file_destination(self, landing_dir: Path, conn_id: str) -> str:
        body = {
            "workspaceId": self.workspace_id,
            "name": f"carbontrace-file-{conn_id[:8]}",
            # destinationDefinitionId for File-based destination — overridden per Airbyte deployment
            "destinationDefinitionId": "9f761074-fc01-44ec-b59c-2c89a2adc8d6",
            "connectionConfiguration": {
                "destination_path": str(landing_dir),
                "format": "JSONL",
            },
        }
        log.info("Airbyte: creating file destination at %s", landing_dir)
        out = self.client._post("/destinations/create", body)  # noqa: SLF001
        return out["destinationId"]

    def _ensure_connection(
        self,
        spec: ConnectorSpec,
        source_id: str,
        destination_id: str,
        conn_id: str,
    ) -> str:
        streams = [
            {
                "stream": {
                    "name": sm.connector_stream,
                    "sourceDefinedCursor": True,
                    "namespace": None,
                },
                "config": {
                    "syncMode": "incremental",
                    "destinationSyncMode": "append",
                    "aliasName": sm.canonical_stream,
                    "selected": True,
                },
            }
            for sm in spec.streams
        ]
        body = {
            "name": f"carbontrace-{spec.key}-{conn_id[:8]}",
            "sourceId": source_id,
            "destinationId": destination_id,
            "syncCatalog": {"streams": streams},
            "scheduleType": "manual",
            "namespaceDefinition": "destination",
            "status": "active",
        }
        log.info("Airbyte: creating connection %s -> %s", source_id, destination_id)
        out = self.client._post("/connections/create", body)  # noqa: SLF001
        return out["connectionId"]


def mark_connection_state(
    connection: ClientConnection,
    result: ProvisioningResult | None = None,
    *,
    status: ConnectionStatus,
    sync: AirbyteSyncResult | None = None,
) -> ClientConnection:
    """Mutates the in-memory connection — caller persists via ConnectionRepository.save()."""
    connection.status = status.value if isinstance(status, ConnectionStatus) else status
    if result:
        connection.airbyte_source_id = result.source_id
        connection.airbyte_destination_id = result.destination_id
        connection.airbyte_connection_id = result.connection_id
        connection.last_landing_dir = str(result.landing_dir)
    if sync:
        connection.last_sync_job_id = sync.job_id
        connection.last_sync_status = sync.status
    return connection
