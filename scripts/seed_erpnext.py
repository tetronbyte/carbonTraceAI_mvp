"""Seed a running ERPNext instance with a factory profile.

Run *after* `docker compose -f docker-compose.erpnext.yml up -d` is up and
http://localhost:8080 is reachable.

    python -m scripts.seed_erpnext --profile mozal_aluminium
    python -m scripts.seed_erpnext --profile ocp_fertiliser --base-url http://localhost:8080

The script:
  1. Calls the ERPNext setup wizard API (if not already done) — this installs
     all standard fixtures (Warehouse Types, Item Groups, Supplier Groups, etc.)
     that a fresh frappe_docker install skips.
  2. Logs in with Administrator / admin (the docker-compose default).
  3. Generates an API key + secret, writes them to .env.erpnext.
  4. Seeds the factory profile data into ERPNext.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import requests

from src.ingestion.erp.erpnext_client import ERPNextClient, ERPNextCredentials
from src.seeding import ERPNextSeeder, get_profile
from src.utils.logger import get_logger

log = get_logger(__name__)

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


def _is_setup_complete(session: requests.Session, base_url: str) -> bool:
    """Check if the ERPNext setup wizard has already been completed."""
    try:
        r = session.get(
            f"{base_url}/api/method/frappe.client.get_value",
            params={"doctype": "System Settings", "fieldname": "setup_complete"},
            timeout=10,
        )
        if r.status_code == 200:
            val = r.json().get("message", {}).get("setup_complete", 0)
            return bool(int(val or 0))
    except Exception:
        pass
    return False


def _run_setup_wizard(session: requests.Session, base_url: str) -> bool:
    """Call the ERPNext setup wizard API to install all standard fixtures.

    A fresh frappe_docker install (bench new-site --install-app erpnext) does
    NOT run the setup wizard, so Warehouse Types, Item Groups, Supplier Groups,
    Customer Groups, and Territories are all missing. Calling setup_complete
    installs all of them in under 30 seconds.

    The company created here ('Sandbox Corp') is a throwaway — the seeder
    creates the real profile company (e.g. 'Mozal SA') separately.
    """
    print("ERPNext setup wizard not yet complete — running now (~20-30 s) ...")
    wizard_args = {
        "language": "English",
        "country": "United States",
        "timezone": "UTC",
        "currency": "USD",
        # Frappe v15 derives first_name from full_name; first_name alone fails
        # with MandatoryError on the new User.
        "full_name": "Sandbox Admin",
        "email": "admin@carbontrace.local",
        "password": "admin",
        "company_name": "Sandbox Corp",
        "company_abbr": "SC",
        "bank_account": "Cash",
        "chart_of_accounts": "Standard",
        "domains": ["Manufacturing"],
    }
    # Try args as a JSON string (older Frappe), then as a plain dict (newer Frappe)
    last_error = ""
    for payload in (
        {"args": json.dumps(wizard_args)},
        {"args": wizard_args},
    ):
        try:
            r = session.post(
                f"{base_url}/api/method/frappe.desk.page.setup_wizard.setup_wizard.setup_complete",
                json=payload,
                timeout=300,
            )
            # Frappe can answer 200 with status=fail, so check the body too.
            if r.status_code in (200, 201) and _is_setup_complete(session, base_url):
                print("Setup wizard complete — standard fixtures installed.")
                return True
            last_error = f"HTTP {r.status_code}: {r.text[:500]}"
        except Exception as exc:
            last_error = str(exc)
    print(f"Setup wizard call failed: {last_error}")
    return False


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
    p.add_argument("--skip-setup-wizard", action="store_true",
                   help="Skip the setup wizard check (if you know it already ran).")
    args = p.parse_args()

    base_url = args.base_url.rstrip("/")

    profile = get_profile(args.profile)
    if args.months is not None:
        profile = type(profile)(**{**profile.__dict__, "months": args.months})
    if args.work_orders_per_month is not None:
        profile = type(profile)(**{**profile.__dict__, "work_orders_per_month": args.work_orders_per_month})
    if args.purchase_orders_per_month is not None:
        profile = type(profile)(**{**profile.__dict__, "purchase_orders_per_month": args.purchase_orders_per_month})

    creds = ERPNextCredentials(
        base_url=base_url,
        username=args.admin_user,
        password=args.admin_pass,
    )
    client = ERPNextClient(creds)

    print(f"Connecting to {base_url} as {args.admin_user} ...")
    client.login_with_password()

    # Step 1 — ensure setup wizard has run (installs all standard fixtures)
    if not args.skip_setup_wizard:
        if _is_setup_complete(client.session, base_url):
            print("ERPNext setup already complete — skipping wizard.")
        else:
            if not _run_setup_wizard(client.session, base_url):
                # Without the wizard there are no Fiscal Years, Stock Entry Types
                # or Price Lists, so transactional docs cannot be created.
                print("Aborting seed: ERPNext setup wizard did not complete.")
                return 1
            # Re-login: wizard resets the session
            client.login_with_password()
            time.sleep(3)   # let ERPNext settle

    # Step 2 — generate API key/secret
    api_key, api_secret = client.ensure_api_keys_for_user(args.admin_user)
    _persist_keys(base_url, api_key, api_secret)
    print(f"API key/secret written to {ENV_FILE}")

    # Step 3 — seed factory data
    seeder = ERPNextSeeder(client, profile, seed=args.seed)
    report = seeder.run()
    print(report.summary())
    if report.errors:
        print(f"\n{len(report.errors)} errors — first 5:")
        for e in report.errors[:5]:
            print(f"  - {e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

