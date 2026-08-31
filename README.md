
---

## Running Locally

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management.

1. **Install dependencies** (from a clean checkout):

   ```bash
   uv sync
   ```

2. **Run the server**:

   ```bash
   uv run uvicorn decodevin.main:app --reload --app-dir src
   ```

   The API will be available at `http://127.0.0.1:8000`. Interactive docs (Swagger UI) are at `http://127.0.0.1:8000/docs`.

3. A SQLite file (`decodevin.db`, path overridable via the `DECODEVIN_DB_PATH` env var) is created automatically in the working directory on first run.

## Running Tests

Tests live in `tests/` and use `pytest` (installed as a dev dependency via `uv sync`).

Each test runs against its own throwaway SQLite database (a `pytest` `tmp_path` fixture), so tests never touch your real `decodevin.db` and can be run in any order without leaving artifacts behind.

Tests are split into two groups:

- **Offline tests** (`test_lookup.py`, `test_remove.py`, `test_export.py`) — mock the vPIC API, so they run fast and don't need internet access.
- **Live tests** (`test_vpic_live.py`) — make real calls to vPIC, tagged with the `network` marker.

```bash
# run everything except the live network tests (fast, no internet needed)
uv run pytest -m "not network"

# run only the live vPIC tests, against every VIN in INSTRUCTIONS.md
uv run pytest -m network

# run every test, including live network calls
uv run pytest
```

### Testing a specific VIN

`test_vpic_live.py` includes a test that accepts any VIN via a custom `--vin` CLI flag, so you can try one of your own without editing the test file:

```bash
uv run pytest tests/test_vpic_live.py::test_lookup_decodes_custom_vin -m network --vin=1HGCM82633A004352
```

If `--vin` isn't passed, that test is skipped rather than failing.