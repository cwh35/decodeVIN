# in-memory byte buffer --> build Parquet file without writing to disk
import io

# used to build a typed, columnar Table in memory
import pyarrow as pa
# used to serialize the Table to Parquet format
import pyarrow.parquet as pq

from decodevin.db import fetch_all


def cache_to_parquet_bytes() -> bytes:
    # get all rows from the database
    rows = fetch_all()

    # fetch all data related to vehicle information
    columns = {
        "vin": [row["vin"] for row in rows],
        "make": [row["make"] for row in rows],
        "model": [row["model"] for row in rows],
        "model_year": [row["model_year"] for row in rows],
        "body_class": [row["body_class"] for row in rows],
    }
    # build the table, declaring every columns as a string
    schema = pa.schema(
        [(name, pa.string()) for name in columns]
    )
    table = pa.table(columns, schema=schema)

    buffer = io.BytesIO()
    pq.write_table(table, buffer) # write parquet table into in-memory buffer
    return buffer.getvalue()
