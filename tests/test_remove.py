from decodevin import db

VALID_VIN = "1HGCM82633A004352"


def test_remove_deletes_cached_vin(client):
    db.insert_cached(VALID_VIN, "HONDA", "Accord", "2003", "Coupe")

    response = client.post("/remove", json={"vin": VALID_VIN})

    assert response.status_code == 200
    assert response.json() == {"vin": VALID_VIN, "cache_delete_success": True}
    assert db.get_cached(VALID_VIN) is None


def test_remove_returns_false_when_vin_not_cached(client):
    """Removing a VIN that was never cached is not an error -- just a false result."""
    response = client.post("/remove", json={"vin": VALID_VIN})

    assert response.status_code == 200
    assert response.json() == {"vin": VALID_VIN, "cache_delete_success": False}


def test_remove_rejects_invalid_vin(client):
    response = client.post("/remove", json={"vin": "short"})
    assert response.status_code == 422
