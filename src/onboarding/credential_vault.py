"""Symmetric encryption for ERP credentials at rest.

Single key from env (`CARBONTRACE_VAULT_KEY` — Fernet base64). For local dev,
auto-generates one and writes it to `data/.vault.key` (gitignored).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken

from config.settings import settings
from src.core.exceptions import CarbonTraceError
from src.utils.logger import get_logger

log = get_logger(__name__)


class VaultError(CarbonTraceError):
    code = "vault_error"


class CredentialVault:
    """Encrypt → bytes → base64 string. Decrypt the inverse."""

    def __init__(self, key: str | None = None) -> None:
        self._key = (key or self._load_or_create_key()).encode()
        try:
            self._fernet = Fernet(self._key)
        except (ValueError, TypeError) as e:
            raise VaultError(f"Invalid Fernet key: {e}") from e

    @staticmethod
    def _load_or_create_key() -> str:
        env_key = os.getenv("CARBONTRACE_VAULT_KEY")
        if env_key:
            return env_key
        key_path: Path = settings.data_dir / ".vault.key"
        if key_path.exists():
            return key_path.read_text().strip()
        new_key = Fernet.generate_key().decode()
        key_path.parent.mkdir(parents=True, exist_ok=True)
        key_path.write_text(new_key)
        try:
            os.chmod(key_path, 0o600)
        except OSError:
            pass
        log.warning(
            "No CARBONTRACE_VAULT_KEY set — auto-generated dev key at %s. "
            "Move to env in production.",
            key_path,
        )
        return new_key

    def encrypt(self, payload: dict[str, Any]) -> str:
        return self._fernet.encrypt(json.dumps(payload).encode()).decode()

    def decrypt(self, token: str) -> dict[str, Any]:
        try:
            return json.loads(self._fernet.decrypt(token.encode()).decode())
        except InvalidToken as e:
            raise VaultError("Vault token is invalid or was encrypted with a different key") from e
