import io

import pyarrow.parquet as pq

from decodevin import db


def test_export_returns_parquet_file_with_cached_data(client):
    db.insert_cached("1HGCM82633A004352", "HONDA", "Accord", "2003", "Coupe")
    db.insert_cached("5YJ3E1EA6PF384836", "TESLA", "Model 3", "2023", "Sedan/Saloon")

    response = client.get("/export")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert "vin_cache.parquet" in response.headers["content-disposition"]

    table = pq.read_table(io.BytesIO(response.content))
    rows = table.to_pylist()

    assert len(rows) == 2
    assert {row["vin"] for row in rows} == {"1HGCM82633A004352", "5YJ3E1EA6PF384836"}


def test_export_returns_valid_empty_parquet_file_when_cache_is_empty(client):
    response = client.get("/export")

    assert response.status_code == 200

    table = pq.read_table(io.BytesIO(response.content))

    assert table.num_rows == 0
    assert table.schema.names == ["vin", "make", "model", "model_year", "body_class"]
