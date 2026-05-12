"""Client connection model — one row per (facility × connector type).

Holds the connector type, masked metadata, encrypted credential blob, and
sync state. The `airbyte_*` fields are populated once Airbyte resources have
been provisioned for this connection.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Column, DateTime, MetaData, String, Table, Text, create_engine, insert, select, update

from config.settings import settings
from src.core.exceptions import ValidationError
from src.utils.logger import get_logger

from .connector_registry import ConnectorSpec, get_connector
from .credential_vault import CredentialVault

log = get_logger(__name__)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class ConnectionStatus(str, Enum):
    DRAFT = "draft"                          # creds saved, not yet provisioned
    PROVISIONED = "provisioned"              # Airbyte source/conn created
    AIRBYTE_UNAVAILABLE = "airbyte_unavailable"  # creds saved but Airbyte unreachable
    SYNCING = "syncing"
    SYNCED = "synced"
    ERRORED = "errored"
    DEPRECATED = "deprecated"


class ClientConnection(BaseModel):
    """In-memory representation. Persisted via ConnectionRepository."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    facility_id: str
    connector_key: str
    display_name: str
    status: ConnectionStatus = ConnectionStatus.DRAFT
    cred_token: str                          # Fernet-encrypted creds blob
    cred_field_names: list[str] = Field(default_factory=list)  # for UI display, never the values
    airbyte_source_id: Optional[str] = None
    airbyte_destination_id: Optional[str] = None
    airbyte_connection_id: Optional[str] = None
    last_sync_job_id: Optional[int] = None
    last_sync_status: Optional[str] = None
    last_landing_dir: Optional[str] = None    # where JSONL lands after a sync
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    @classmethod
    def from_creds(
        cls,
        *,
        facility_id: str,
        connector_key: str,
        creds: dict[str, Any],
        vault: CredentialVault,
        notes: str | None = None,
    ) -> "ClientConnection":
        spec = get_connector(connector_key)
        cls._validate_creds(spec, creds)
        return cls(
            facility_id=facility_id,
            connector_key=spec.key,
            display_name=spec.display_name,
            cred_token=vault.encrypt(creds),
            cred_field_names=[f.name for f in spec.credentials],
            notes=notes,
        )

    @staticmethod
    def _validate_creds(spec: ConnectorSpec, creds: dict[str, Any]) -> None:
        missing = [f.name for f in spec.credentials if f.required and not creds.get(f.name)]
        if missing:
            raise ValidationError(
                f"Connector {spec.key!r} missing required credential fields: {missing}",
                missing=missing,
            )

    def reveal_credentials(self, vault: CredentialVault) -> dict[str, Any]:
        """Decrypt — only call inside the provisioner / ingestor boundary."""
        return vault.decrypt(self.cred_token)


# --------------------------------------------------------------------------
# Persistence
# --------------------------------------------------------------------------
class ConnectionRepository:
    """Standalone repo for client connections. Same SQLite file as canonical store."""

    def __init__(self, db_url: str | None = None) -> None:
        self.engine = create_engine(db_url or settings.db_url, future=True)
        self.metadata = MetaData()
        self.table = Table(
            "client_connections",
            self.metadata,
            Column("id", String, primary_key=True),
            Column("facility_id", String, index=True),
            Column("connector_key", String, index=True),
            Column("display_name", String),
            Column("status", String, index=True),
            Column("cred_token", Text, nullable=False),
            Column("cred_field_names", Text),       # JSON array
            Column("airbyte_source_id", String),
            Column("airbyte_destination_id", String),
            Column("airbyte_connection_id", String),
            Column("last_sync_job_id", String),
            Column("last_sync_status", String),
            Column("last_landing_dir", String),
            Column("notes", Text),
            Column("created_at", DateTime),
            Column("updated_at", DateTime),
        )
        self.metadata.create_all(self.engine)

    # --- writes ---
    def save(self, conn: ClientConnection) -> ClientConnection:
        conn.updated_at = _utcnow()
        row = conn.model_dump()
        row["cred_field_names"] = json.dumps(row["cred_field_names"])
        with self.engine.begin() as db:
            existing = db.execute(select(self.table.c.id).where(self.table.c.id == conn.id)).scalar()
            if existing:
                db.execute(update(self.table).where(self.table.c.id == conn.id).values(**row))
            else:
                db.execute(insert(self.table), [row])
        return conn

    # --- reads ---
    def get(self, connection_id: str) -> Optional[ClientConnection]:
        with self.engine.connect() as db:
            row = db.execute(select(self.table).where(self.table.c.id == connection_id)).mappings().first()
        return self._hydrate(row) if row else None

    def list_by_facility(self, facility_id: str) -> list[ClientConnection]:
        with self.engine.connect() as db:
            rows = db.execute(
                select(self.table).where(self.table.c.facility_id == facility_id)
            ).mappings().all()
        return [self._hydrate(r) for r in rows]

    def list_all(self) -> list[ClientConnection]:
        with self.engine.connect() as db:
            rows = db.execute(select(self.table)).mappings().all()
        return [self._hydrate(r) for r in rows]

    def _hydrate(self, row: dict) -> ClientConnection:
        d = dict(row)
        if isinstance(d.get("cred_field_names"), str):
            try:
                d["cred_field_names"] = json.loads(d["cred_field_names"])
            except json.JSONDecodeError:
                d["cred_field_names"] = []
        return ClientConnection(**d)
