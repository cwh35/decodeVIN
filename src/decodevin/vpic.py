import os

import httpx

VPIC_BASE_URL = os.environ.get(
    "VPIC_BASE_URL", "https://vpic.nhtsa.dot.gov/api/vehicles"
)
VPIC_TIMEOUT_SECONDS = float(os.environ.get("VPIC_TIMEOUT_SECONDS", "10"))

_WANTED_FIELDS = {
    "Make": "make",
    "Model": "model",
    "Model Year": "model_year",
    "Body Class": "body_class",
}


class VpicError(Exception):
    """Raised when the vPIC API can't be reached or returns something unusable."""


async def decode_vin(vin: str) -> dict:
    url = f"{VPIC_BASE_URL}/decodevin/{vin}?format=json"

    try:
        async with httpx.AsyncClient(timeout=VPIC_TIMEOUT_SECONDS) as client:
            response = await client.get(url)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise VpicError(f"vPIC API request failed: {exc}") from exc

    payload = response.json()
    results = payload.get("Results", [])

    decoded = {field: "" for field in _WANTED_FIELDS.values()}
    for item in results:
        key = _WANTED_FIELDS.get(item.get("Variable"))
        if key is not None:
            decoded[key] = item.get("Value") or ""

    if not decoded["make"] and not decoded["model"]:
        raise VpicError(f"vPIC could not decode VIN {vin}")

    return decoded
