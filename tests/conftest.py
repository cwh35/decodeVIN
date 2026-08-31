import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from decodevin import db
from decodevin.main import app


def pytest_addoption(parser):
    parser.addoption(
        "--vin",
        action="store",
        default=None,
        help=(
            "Run the live-vPIC custom-VIN test against this VIN, e.g. "
            "pytest -m network --vin=1HGCM82633A004352"
        ),
    )


@pytest.fixture
def custom_vin(request):
    return request.config.getoption("--vin")


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    """Point every test at its own throwaway SQLite file instead of the real decodevin.db."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.init_db()
    yield db_path


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
