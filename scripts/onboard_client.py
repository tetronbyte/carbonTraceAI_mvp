"""Client onboarding CLI demo.

Walks through:
  1. listing supported connectors
  2. picking one (interactive or --connector flag)
  3. entering credentials (interactive)
  4. saving an encrypted ClientConnection
  5. running a sync via ErpConnectorFactory

For a non-interactive demo, pass the creds via `--base-url --api-key --api-secret`.
"""
from __future__ import annotations

import argparse
import getpass
from typing import Any

from rich.console import Console
from rich.table import Table

from src.onboarding import (
    AirbyteProvisioner,
    ClientConnection,
    ConnectionRepository,
    CredentialVault,
    ErpConnectorFactory,
    get_connector,
    list_connectors,
)
from src.storage.repository import Repository

console = Console()


def show_connector_table() -> None:
    t = Table(title="Supported ERP connectors", show_lines=False)
    t.add_column("#", justify="right")
    t.add_column("key")
    t.add_column("vendor")
    t.add_column("name")
    t.add_column("airbyte source id", overflow="fold")
    for i, spec in enumerate(list_connectors(), 1):
        t.add_row(str(i), spec.key, spec.vendor, spec.display_name,
                  spec.airbyte_source_definition_id or "—")
    console.print(t)


def collect_credentials(connector_key: str, presets: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = get_connector(connector_key)
    presets = presets or {}
    creds: dict[str, Any] = {}
    console.print(f"[bold]Enter credentials for {spec.display_name}[/bold]")
    for f in spec.credentials:
        if f.name in presets:
            creds[f.name] = presets[f.name]
            continue
        prompt = f"  {f.label}{' (required)' if f.required else ''}"
        if f.placeholder:
            prompt += f" [dim]e.g. {f.placeholder}[/dim]"
        prompt += ": "
        if f.secret:
            value = getpass.getpass(prompt)
        else:
            value = console.input(prompt)
        if value:
            creds[f.name] = value
    return creds


def main() -> int:
    p = argparse.ArgumentParser(description="Onboard a client ERP connection.")
    p.add_argument("--facility-id", default="MOZAL-MZ-01")
    p.add_argument("--connector", default="erpnext_direct",
                   help="Connector key. Use --list to show options.")
    p.add_argument("--list", action="store_true", help="List connectors and exit.")
    p.add_argument("--no-sync", action="store_true", help="Save the connection but don't sync.")
    p.add_argument("--base-url",   help="Pre-fill ERPNext base URL (skip prompt).")
    p.add_argument("--api-key",    help="Pre-fill ERPNext API key (skip prompt).")
    p.add_argument("--api-secret", help="Pre-fill ERPNext API secret (skip prompt).")
    args = p.parse_args()

    if args.list:
        show_connector_table()
        return 0

    spec = get_connector(args.connector)
    presets: dict[str, Any] = {}
    if args.base_url:   presets["base_url"]   = args.base_url
    if args.api_key:    presets["api_key"]    = args.api_key
    if args.api_secret: presets["api_secret"] = args.api_secret
    if presets and all(f.name in presets for f in spec.credentials if f.required):
        creds = presets
    else:
        creds = collect_credentials(args.connector, presets=presets)

    vault = CredentialVault()
    connections = ConnectionRepository()
    repo = Repository()

    conn = ClientConnection.from_creds(
        facility_id=args.facility_id,
        connector_key=args.connector,
        creds=creds,
        vault=vault,
        notes=f"Onboarded via CLI ({args.connector})",
    )
    connections.save(conn)
    console.print(f"[green]Saved connection[/green] id={conn.id} status={conn.status}")

    if args.no_sync:
        console.print("[dim]--no-sync set; skipping sync.[/dim]")
        return 0

    factory = ErpConnectorFactory(
        repository=repo,
        connections=connections,
        vault=vault,
        provisioner=AirbyteProvisioner(),
        simulate_when_unavailable=True,
    )
    outcome = factory.sync(conn.id)
    console.print(outcome.summary())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
