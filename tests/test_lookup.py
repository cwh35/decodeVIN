import pytest

from decodevin import db
from decodevin.vpic import VpicError

VALID_VIN = "1HGCM82633A004352"

SAMPLE_DECODED = {
    "make": "HONDA",
    "model": "Accord",
    "model_year": "2003",
    "body_class": "Coupe",
}


async def _fake_decode_vin(vin: str) -> dict:
    return SAMPLE_DECODED


def test_lookup_adds_new_vin_to_database(client, monkeypatch):
    """A cache miss should call vPIC, persist the result, and return it with cached=False."""
    monkeypatch.setattr("decodevin.main.decode_vin", _fake_decode_vin)

    response = client.post("/lookup", json={"vin": VALID_VIN})

    assert response.status_code == 200
    assert response.json() == {
        "vin": VALID_VIN,
        "make": "HONDA",
        "model": "Accord",
        "model_year": "2003",
        "body_class": "Coupe",
        "cached": False,
    }

    # confirm it actually landed in the database, not just the HTTP response
    row = db.get_cached(VALID_VIN)
    assert row is not None
    assert row["make"] == "HONDA"


def test_lookup_returns_cached_result_on_second_call(client, monkeypatch):
    """A second /lookup for the same VIN should hit the cache and never call vPIC again."""
    calls = []

    async def counting_decode_vin(vin: str) -> dict:
        calls.append(vin)
        return SAMPLE_DECODED

    monkeypatch.setattr("decodevin.main.decode_vin", counting_decode_vin)

    first = client.post("/lookup", json={"vin": VALID_VIN})
    second = client.post("/lookup", json={"vin": VALID_VIN})

    assert first.json()["cached"] is False
    assert second.json()["cached"] is True
    assert len(calls) == 1


@pytest.mark.parametrize(
    "vin",
    [
        "SHORT",  # too short
        "1HGCM82633A0043521",  # too long (18 chars)
        "1HGCM8263!A004352",  # contains a non-alphanumeric character
        "",  # empty string
    ],
)
def test_lookup_rejects_invalid_vin(client, vin):
    response = client.post("/lookup", json={"vin": vin})
    assert response.status_code == 422


def test_lookup_rejects_missing_vin_field(client):
    response = client.post("/lookup", json={})
    assert response.status_code == 422


def test_lookup_returns_502_when_vpic_fails(client, monkeypatch):
    """If vPIC can't be reached or can't decode the VIN, /lookup should surface a 502, not a 500."""

    async def failing_decode_vin(vin: str) -> dict:
        raise VpicError("vPIC API request failed: timeout")

    monkeypatch.setattr("decodevin.main.decode_vin", failing_decode_vin)

    response = client.post("/lookup", json={"vin": VALID_VIN})

    assert response.status_code == 502
    assert "vPIC" in response.json()["detail"]

    # a failed decode should never be cached
    assert db.get_cached(VALID_VIN) is None
