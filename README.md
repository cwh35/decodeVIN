
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