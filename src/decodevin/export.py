import io

import pyarrow as pa
import pyarrow.parquet as pq

from decodevin.db import fetch_all


def cache_to_parquet_bytes() -> bytes:
    rows = fetch_all()

    # fetch all data related to vehicle information
    columns = {
        "vin": [row["vin"] for row in rows],
        "make": [row["make"] for row in rows],
        "model": [row["model"] for row in rows],
        "model_year": [row["model_year"] for row in rows],
        "body_class": [row["body_class"] for row in rows],
    }
    schema = pa.schema(
        [(name, pa.string()) for name in columns]
    )
    table = pa.table(columns, schema=schema)

    buffer = io.BytesIO()
    pq.write_table(table, buffer)
    return buffer.getvalue()
