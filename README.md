# NAS Backend Coding Challenge

## Objective

Implement a simple FastAPI backend to decode VINs, powered by the vPIC API and backed by a SQLite cache.

## Time

Take as much time as you need. We aren't timing you, and we'd rather see something you're comfortable talking through than something rushed.

## On Using AI

Using AI coding assistants (Claude, Copilot, Cursor, ChatGPT, etc.) is completely fine — use whatever tools you'd use on a normal workday.

What matters is that you can stand behind what you submit. When we review this together, we're going to spend most of our time talking through the code: why you structured it the way you did, what the tradeoffs were, what you'd change if this had to handle real traffic, and where the weak spots are. If your assistant made a decision you didn't think about, that will show up quickly in the conversation.

Put differently: the conversation about the assignment matters more to us than the finished artifact. A modest implementation you understand deeply will do better here than a polished one you can't explain.

## Requirements

Your application should contain three (3) routes:

### `/lookup`

This route will first check the SQLite database to see if a cached result is available. If so, it should be returned from the database.

If not, your API should contact the vPIC API to decode the VIN, store the results in the database, and return the result.

The request should contain a single string called `vin`. It should contain exactly 17 alphanumeric characters.

The response object should contain the following elements:

- Input VIN Requested (string, exactly 17 alphanumeric characters)
- Make (string)
- Model (string)
- Model Year (string)
- Body Class (string)
- Cached Result? (boolean)

### `/remove`

This route will remove an entry from the cache.

The request should contain a single string called `vin`. It should contain exactly 17 alphanumeric characters.

The response object should contain the following elements:

- Input VIN Requested (string, exactly 17 alphanumeric characters)
- Cache Delete Success? (boolean)

### `/export`

This route will export the SQLite database cache and return a binary file (Parquet format) containing the data in the cache.

No additional input/data should be required to make the request.

The response object should be a binary file downloaded by the client containing all currently cached VINs in a table stored in Parquet format.

## Build, Setup, and Deploy

- Use FastAPI as your web framework. You may structure your project as you wish.
- You do not need to deploy your code, but you should be prepared to have a conversation about how to do so.
- Include instructions in your README for getting the service running locally from a clean checkout.
- Also include a short `NOTES.md` alongside your code. What goes in it is up to you — a page or less of whatever you think is worth telling us about what you built.

## Submitting Your Work

When you're ready, push your work to a GitHub repo and send us the link.

The repo needs to be either public, or private and shared with the GitHub user `atkincaid74`. If you were given different submission instructions along with this challenge, follow those instead.

## Our Evaluation

- Basic functionality
- Code quality
- Error handling
- Documentation (readme/comments/tests)
- Ability to explain your implementation decisions

Please feel free to be creative and add any embellishments or additional functionality you would like to show off!

## Test VINs

You may use the following test VINs. We encourage you to try VINs you may find from other sources!

```
1HGCM82633A004352
5YJ3E1EA6PF384836
1FTFW1ET9DFC10312
1C4RJFBG2FC625797
5FNRL6H79NB021411
1HD1KBM15FB620271
1XPWD40X1ED215307
```

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

### Example requests

**macOS/Linux (bash)**

```bash
curl -X POST http://127.0.0.1:8000/lookup -H "Content-Type: application/json" -d '{"vin":"1HGCM82633A004352"}'
curl -X POST http://127.0.0.1:8000/remove -H "Content-Type: application/json" -d '{"vin":"1HGCM82633A004352"}'
curl -o cache.parquet http://127.0.0.1:8000/export
```

**Windows (PowerShell)**

`curl` is aliased to `Invoke-WebRequest` in PowerShell, which doesn't accept `-X`/`-H`/`-d` the way real curl does. Use the native cmdlets instead:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/lookup -ContentType "application/json" -Body '{"vin":"1HGCM82633A004352"}'
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/remove -ContentType "application/json" -Body '{"vin":"1HGCM82633A004352"}'
Invoke-WebRequest -Uri http://127.0.0.1:8000/export -OutFile cache.parquet
```

Or call the real curl binary explicitly with `curl.exe`, escaping inner quotes:

```powershell
curl.exe -X POST http://127.0.0.1:8000/lookup -H "Content-Type: application/json" -d '{\"vin\":\"1HGCM82633A004352\"}'
```

You can also skip the command line entirely and use the interactive Swagger UI at `http://127.0.0.1:8000/docs`.

---

See [`NOTES.md`](NOTES.md) for design notes, tradeoffs, and what I'd change for production traffic.
