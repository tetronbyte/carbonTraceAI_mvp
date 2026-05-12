"""ERPNext (Frappe) REST API client.

Talks to any ERPNext instance — local Docker, ngrok-tunnelled, or production.
Uses the Frappe v15+ REST API:
  - Auth: `Authorization: token <api_key>:<api_secret>`
  - Read:  /api/method/frappe.client.get_list, /api/resource/<DocType>[/<name>]
  - Write: POST /api/resource/<DocType>, PUT /api/resource/<DocType>/<name>
  - Login (for seeding): POST /api/method/login

The client only depends on `requests` (already in requirements.txt) and stdlib.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterator, Optional

import requests

from src.core.exceptions import IngestionError
from src.utils.logger import get_logger

log = get_logger(__name__)


@dataclass
class ERPNextCredentials:
    base_url: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    # Fallback: username/password for the seed script (where API keys aren't
    # provisioned yet). For ingestion we always prefer the token pair.
    username: Optional[str] = None
    password: Optional[str] = None

    def normalised_url(self) -> str:
        return self.base_url.rstrip("/")


class ERPNextClient:
    """Thin REST wrapper. Chunked iteration is built-in for large pulls."""

    def __init__(
        self,
        creds: ERPNextCredentials,
        timeout: int = 30,
        verify_tls: bool = True,
    ) -> None:
        self.creds = creds
        self.timeout = timeout
        self.session = requests.Session()
        self.session.verify = verify_tls
        if creds.api_key and creds.api_secret:
            self.session.headers.update({
                "Authorization": f"token {creds.api_key}:{creds.api_secret}",
            })
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    # ---- auth ----------------------------------------------------------------
    def login_with_password(self) -> None:
        """Used by the seed script when no API key has been issued yet."""
        if not (self.creds.username and self.creds.password):
            raise IngestionError("login_with_password requires username + password")
        url = f"{self.creds.normalised_url()}/api/method/login"
        r = self.session.post(
            url,
            data={"usr": self.creds.username, "pwd": self.creds.password},
            timeout=self.timeout,
        )
        r.raise_for_status()
        log.info("ERPNext: logged in as %s", self.creds.username)

    def ensure_api_keys_for_user(self, user: str = "Administrator") -> tuple[str, str]:
        """Generate (or refresh) API key + secret for a user, return both.
        Requires an authenticated session (login_with_password first)."""
        url = f"{self.creds.normalised_url()}/api/method/frappe.core.doctype.user.user.generate_keys"
        r = self.session.post(url, json={"user": user}, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        api_secret = data.get("message", {}).get("api_secret")
        if not api_secret:
            raise IngestionError(f"Failed to generate API secret: {data}")
        # api_key sits on the User doctype
        user_doc = self.get_doc("User", user)
        api_key = user_doc.get("api_key")
        if not api_key:
            raise IngestionError("User has no api_key after generate_keys call")
        # bind the new token to this client
        self.creds.api_key = api_key
        self.creds.api_secret = api_secret
        self.session.headers["Authorization"] = f"token {api_key}:{api_secret}"
        return api_key, api_secret

    # ---- reads ---------------------------------------------------------------
    def ping(self) -> bool:
        """Quick health probe used by the factory before a sync."""
        try:
            url = f"{self.creds.normalised_url()}/api/method/frappe.client.get_value"
            r = self.session.get(
                url,
                params={
                    "doctype": "User",
                    "fieldname": "name",
                    "filters": json.dumps({"name": "Administrator"}),
                },
                timeout=5,
            )
            return r.status_code == 200
        except requests.RequestException:
            return False

    def get_list(
        self,
        doctype: str,
        fields: list[str] | None = None,
        filters: list | dict | None = None,
        limit: int = 100,
        start: int = 0,
        order_by: str = "modified desc",
    ) -> list[dict[str, Any]]:
        url = f"{self.creds.normalised_url()}/api/method/frappe.client.get_list"
        params: dict[str, Any] = {
            "doctype": doctype,
            "limit_page_length": limit,
            "limit_start": start,
            "order_by": order_by,
        }
        if fields:
            params["fields"] = json.dumps(fields)
        if filters:
            params["filters"] = json.dumps(filters)
        r = self.session.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json().get("message", [])

    def get_doc(self, doctype: str, name: str) -> dict[str, Any]:
        url = f"{self.creds.normalised_url()}/api/resource/{doctype}/{name}"
        r = self.session.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json().get("data", {})

    def iter_all(
        self,
        doctype: str,
        fields: list[str] | None = None,
        filters: list | dict | None = None,
        page_size: int = 200,
    ) -> Iterator[dict[str, Any]]:
        start = 0
        while True:
            batch = self.get_list(
                doctype, fields=fields, filters=filters,
                limit=page_size, start=start,
            )
            if not batch:
                return
            yield from batch
            if len(batch) < page_size:
                return
            start += page_size

    def get_count(self, doctype: str, filters: dict | list | None = None) -> int:
        url = f"{self.creds.normalised_url()}/api/method/frappe.client.get_count"
        params: dict[str, Any] = {"doctype": doctype}
        if filters:
            params["filters"] = json.dumps(filters)
        r = self.session.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return int(r.json().get("message", 0))

    # ---- writes (used by seed script) ---------------------------------------
    def insert(self, doctype: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.creds.normalised_url()}/api/resource/{doctype}"
        r = self.session.post(url, json=payload, timeout=self.timeout)
        if r.status_code >= 400:
            raise IngestionError(
                f"ERPNext insert {doctype} failed: {r.status_code} {r.text[:300]}",
                doctype=doctype, status_code=r.status_code,
            )
        return r.json().get("data", {})

    def upsert(self, doctype: str, payload: dict[str, Any], name_field: str = "name") -> dict[str, Any]:
        """Insert if missing, else PUT update."""
        name = payload.get(name_field)
        if name:
            try:
                existing = self.get_doc(doctype, name)
            except requests.HTTPError as exc:
                existing = None if exc.response is not None and exc.response.status_code == 404 else None
                if existing is None:
                    return self.insert(doctype, payload)
            if existing:
                url = f"{self.creds.normalised_url()}/api/resource/{doctype}/{name}"
                r = self.session.put(url, json=payload, timeout=self.timeout)
                r.raise_for_status()
                return r.json().get("data", {})
        return self.insert(doctype, payload)

    def submit(self, doctype: str, name: str) -> None:
        """Frappe documents move from draft to submitted. Many manufacturing
        doctypes (Work Order, Stock Entry, Sales Invoice) need this."""
        url = f"{self.creds.normalised_url()}/api/method/frappe.client.submit"
        r = self.session.post(
            url,
            json={"doc": json.dumps({"doctype": doctype, "name": name})},
            timeout=self.timeout,
        )
        if r.status_code >= 400:
            log.warning("submit %s/%s failed: %s", doctype, name, r.text[:200])

    def call_method(self, method_path: str, params: dict[str, Any] | None = None) -> Any:
        """Invoke an arbitrary whitelisted Frappe method (e.g. for custom-field setup)."""
        url = f"{self.creds.normalised_url()}/api/method/{method_path}"
        r = self.session.post(url, json=params or {}, timeout=self.timeout)
        r.raise_for_status()
        return r.json().get("message")
