import os
import sys
from pathlib import Path

# Make the repo root importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Use a per-process temp DB to avoid clobbering local data
os.environ.setdefault("CARBONTRACE_DB_URL", "sqlite:///./data/carbontrace_test.db")

import pytest
from src.storage.repository import Repository


@pytest.fixture()
def repo(tmp_path):
    db_url = f"sqlite:///{tmp_path / 'test.db'}"
    return Repository(db_url=db_url)
