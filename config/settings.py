"""Central settings — read from env, with sensible defaults for local dev."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    project_root: Path = PROJECT_ROOT
    data_dir: Path = Path(os.getenv("CARBONTRACE_DATA_DIR", PROJECT_ROOT / "data"))
    db_url: str = os.getenv(
        "CARBONTRACE_DB_URL", f"sqlite:///{PROJECT_ROOT / 'data' / 'carbontrace.db'}"
    )
    log_level: str = os.getenv("CARBONTRACE_LOG_LEVEL", "INFO")
    tesseract_cmd: str | None = os.getenv("TESSERACT_CMD")

    airbyte_api_url: str = os.getenv("AIRBYTE_API_URL", "http://localhost:8000/api/v1")
    airbyte_username: str = os.getenv("AIRBYTE_USERNAME", "airbyte")
    airbyte_password: str = os.getenv("AIRBYTE_PASSWORD", "password")

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def staged_dir(self) -> Path:
        return self.data_dir / "staged"

    @property
    def samples_dir(self) -> Path:
        return self.data_dir / "samples"

    @property
    def schemas_dir(self) -> Path:
        return self.project_root / "config" / "schemas"

    @property
    def data_dictionary_path(self) -> Path:
        return self.project_root / "config" / "data_dictionary.yaml"

    def ensure_dirs(self) -> None:
        for p in (self.data_dir, self.raw_dir, self.staged_dir, self.samples_dir):
            p.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_dirs()
