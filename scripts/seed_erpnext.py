"""Seed a running ERPNext instance with a factory profile.

Run *after* `docker compose -f docker-compose.erpnext.yml up -d` is up and
http://localhost:8080 is reachable.

    python -m scripts.seed_erpnext --profile mozal_aluminium
    python -m scripts.seed_erpnext --profile ocp_fertiliser --base-url http://localhost:8080

The script logs in with Administrator / admin (the docker-compose default),
generates an API key + secret, and writes them to .env.erpnext so the
ingestion pipeline can pick them up later.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from src.ingestion.erp.erpnext_client import ERPNextClient, ERPNextCredentials
from src.seeding import ERPNextSeeder, get_profile

ENV_FILE = Path(".env.erpnext")


def _persist_keys(base_url: str, api_key: str, api_secret: str) -> None:
    ENV_FILE.write_text(
        "# Auto-written by scripts/seed_erpnext.py\n"
        f"ERPNEXT_BASE_URL={base_url}\n"
        f"ERPNEXT_API_KEY={api_key}\n"
        f"ERPNEXT_API_SECRET={api_secret}\n"
    )
    try:
        os.chmod(ENV_FILE, 0o600)
    except OSError:
        pass


def main() -> int:
    p = argparse.ArgumentParser(description="Seed ERPNext with a CBAM factory profile.")
    p.add_argument("--profile", choices=("mozal_aluminium", "ocp_fertiliser"),
                   default="mozal_aluminium")
    p.add_argument("--base-url", default="http://localhost:8080")
    p.add_argument("--admin-user", default="Administrator")
    p.add_argument("--admin-pass", default="admin")
    p.add_argument("--months", type=int, default=None,
                   help="Override profile month count (smoke tests).")
    p.add_argument("--work-orders-per-month", type=int, default=None)
    p.add_argument("--purchase-orders-per-month", type=int, default=None)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    profile = get_profile(args.profile)
    if args.months is not None:
        profile = type(profile)(**{**profile.__dict__, "months": args.months})
    if args.work_orders_per_month is not None:
        profile = type(profile)(**{**profile.__dict__, "work_orders_per_month": args.work_orders_per_month})
    if args.purchase_orders_per_month is not None:
        profile = type(profile)(**{**profile.__dict__, "purchase_orders_per_month": args.purchase_orders_per_month})

    creds = ERPNextCredentials(
        base_url=args.base_url,
        username=args.admin_user,
        password=args.admin_pass,
    )
    client = ERPNextClient(creds)

    print(f"Connecting to {args.base_url} as {args.admin_user} ...")
    client.login_with_password()
    api_key, api_secret = client.ensure_api_keys_for_user(args.admin_user)
    _persist_keys(args.base_url, api_key, api_secret)
    print(f"API key/secret written to {ENV_FILE}")

    seeder = ERPNextSeeder(client, profile, seed=args.seed)
    report = seeder.run()
    print(report.summary())
    if report.errors:
        print(f"\n{len(report.errors)} errors — first 5:")
        for e in report.errors[:5]:
            print(f"  - {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
