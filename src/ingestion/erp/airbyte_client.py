"""Thin Airbyte API client used by the AirbyteProvisioner.

Active in two scenarios:
  - ERPNext via Airbyte (preferred for production)
  - Any other Tier-1 ERP in the registry (SAP, Oracle, Dynamics, NetSuite, Sage, Odoo)

For local demos the direct `ERPNextClient` is used instead — same canonical
JSONL lands either way, so the downstream ErpIngestor is unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from config.settings import settings
from src.utils.logger import get_logger

log = get_logger(__name__)


@dataclass
class AirbyteSyncResult:
    job_id: int
    status: str


class AirbyteClient:
    def __init__(
        self,
        api_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout: int = 30,
    ) -> None:
        self.api_url = (api_url or settings.airbyte_api_url).rstrip("/")
        self.auth = (username or settings.airbyte_username, password or settings.airbyte_password)
        self.timeout = timeout

    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.api_url}{path}"
        resp = requests.post(url, json=body, auth=self.auth, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def list_connections(self, workspace_id: str) -> list[dict[str, Any]]:
        return self._post("/connections/list", {"workspaceId": workspace_id}).get("connections", [])

    def trigger_sync(self, connection_id: str) -> AirbyteSyncResult:
        log.info("Triggering Airbyte sync for connection %s", connection_id)
        out = self._post("/connections/sync", {"connectionId": connection_id})
        job = out.get("job", {})
        return AirbyteSyncResult(job_id=job.get("id"), status=job.get("status", "unknown"))

    def get_job(self, job_id: int) -> dict[str, Any]:
        return self._post("/jobs/get", {"id": job_id})
