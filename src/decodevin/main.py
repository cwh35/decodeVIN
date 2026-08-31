from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response
# streaming response: used for arbitrary bytes with a custom content type
from fastapi.responses import StreamingResponse

from decodevin import db
from decodevin.export import cache_to_parquet_bytes
from decodevin.schemas import LookupResponse, RemoveResponse, VinRequest
from decodevin.vpic import VpicError, decode_vin


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="decodeVIN", lifespan=lifespan)

# get vehicle info from VIN, cache it, and return the info
@app.post("/lookup", response_model=LookupResponse)
async def lookup(request: VinRequest) -> LookupResponse:
    # check if the VIN is already cached in the database
    cached = db.get_cached(request.vin)
    if cached is not None:
        return LookupResponse(
            vin=cached["vin"],
            make=cached["make"],
            model=cached["model"],
            model_year=cached["model_year"],
            body_class=cached["body_class"],
            cached=True,
        )

    try:
        # if not cached, call vPIC API to decode the VIN
        decoded = await decode_vin(request.vin)
    # raised either on an HTTP failure or undecodable VIN
    except VpicError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    # insert the decoded VIN info into the database cache
    db.insert_cached(
        request.vin,
        decoded["make"],
        decoded["model"],
        decoded["model_year"],
        decoded["body_class"],
    )

    # return the decoded VIN info in the response
    return LookupResponse(
        vin=request.vin,
        make=decoded["make"],
        model=decoded["model"],
        model_year=decoded["model_year"],
        body_class=decoded["body_class"],
        cached=False,
    )


@app.post("/remove", response_model=RemoveResponse)
async def remove(request: VinRequest) -> RemoveResponse:
    deleted = db.delete_cached(request.vin)
    return RemoveResponse(vin=request.vin, cache_delete_success=deleted)


@app.get("/export")
async def export() -> Response:
    parquet_bytes = cache_to_parquet_bytes()
    return StreamingResponse(
        iter([parquet_bytes]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=vin_cache.parquet"},
    )
