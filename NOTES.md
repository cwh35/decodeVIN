# VIN API

## Routes

| Route | Description |
|---|---|
| `/lookup` | Retrieves VIN info from the database cache, or uses the vPIC API to decode the VIN |
| `/remove` | Removes a VIN from the database cache |
| `/export` | Extracts VIN info from the database cache and exports a Parquet file |

## Files

| File | Description |
|---|---|
| `main.py` | Contains all the routes for the decodeVIN API |
| `db.py` | Contains logic for accessing the SQLite database via insert, delete, and select |
| `schemas.py` | Contains the structure of the response and request objects for the API endpoints |
| `vpic.py` | Contains the logic for hitting the vPIC API and decoding VINs |
| `export.py` | Contains the logic for exporting the cached VIN data into a Parquet file |

## Tests

| File | Description |
|---|---|
| `conftest.py` | Provides shared testing setup that the other test files pull in automatically (doesn't need to be imported) |
| `test_lookup.py` | Tests adding a new VIN (not in cache), cache hit on second call, 4 invalid VIN cases (too short, too long, non-alphanumeric, empty), missing field, and vPIC failure (502) |
| `test_remove.py` | Tests successful delete, delete-on-a-miss, and invalid VIN rejection |
| `test_export.py` | Tests a Parquet file with cached rows, and an empty-cache export |
| `test_vpic_live.py` | Tests real (unmocked) calls to vPIC for all 7 VINs in `INSTRUCTIONS.md`, plus a `--vin` flag for testing any VIN |
