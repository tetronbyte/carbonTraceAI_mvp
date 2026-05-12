"""Raw landing zone — JSONL writer mirroring Airbyte's file destination layout.

Path: data/raw/<source>/<stream>/<run_ts>.jsonl
Each line is a single raw record as emitted by the source. The canonical
models reference back via `raw_ref = "<jsonl_path>:<line_no>"`.
"""
from __future__ import annotations

import json
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, TextIO

from config.settings import settings


class RawLandingZone:
    def __init__(self, source: str, stream: str, run_ts: datetime | None = None) -> None:
        self.source = source
        self.stream = stream
        self.run_ts = run_ts or datetime.now(timezone.utc).replace(tzinfo=None)
        self.path: Path = (
            settings.raw_dir
            / source.lower()
            / stream
            / f"{self.run_ts.strftime('%Y%m%dT%H%M%S')}.jsonl"
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def open(self) -> Iterator["_LandingWriter"]:
        with self.path.open("w", encoding="utf-8") as fh:
            yield _LandingWriter(fh, self.path)


class _LandingWriter:
    def __init__(self, fh: TextIO, path: Path) -> None:
        self._fh = fh
        self._path = path
        self._line_no = 0

    def write(self, record: dict[str, Any]) -> str:
        """Append one record. Return raw_ref pointer for canonical models."""
        self._fh.write(json.dumps(record, default=str) + "\n")
        self._line_no += 1
        return f"{self._path}:{self._line_no}"

    @property
    def path(self) -> Path:
        return self._path
