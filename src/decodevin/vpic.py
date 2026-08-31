# file for reaching out to the vPIC API and decoding VINs
import os
import httpx

# set the url for the vPIC API
VPIC_BASE_URL = os.environ.get(
    "VPIC_BASE_URL", "https://vpic.nhtsa.dot.gov/api/vehicles"
)
# set the timeout for the vPIC API to 10 seconds
VPIC_TIMEOUT_SECONDS = float(os.environ.get("VPIC_TIMEOUT_SECONDS", "10"))

# fields that we want to extract from the vin decoding results
# key-value pairs (from the docs)
_WANTED_FIELDS = {
    "Make": "make",
    "Model": "model",
    "Model Year": "model_year",
    "Body Class": "body_class",
}


class VpicError(Exception):
    """Raised when the vPIC API can't be reached or returns something invalid"""


async def decode_vin(vin: str) -> dict:
    url = f"{VPIC_BASE_URL}/decodevin/{vin}?format=json"

    try:
        # make an async request to the vPIC API
        async with httpx.AsyncClient(timeout=VPIC_TIMEOUT_SECONDS) as client:
            response = await client.get(url)
        response.raise_for_status() # raise http error if status is a 400 or 500 code
    except httpx.HTTPError as exc:
        raise VpicError(f"vPIC API request failed: {exc}") from exc

    # returns the response as example ---> { "Value": "BMW", "Variable": "Make", "VariableId": 26, "ValueId": 440 }
    payload = response.json()
    # api returns an array of objects with the key "Results"
    results = payload.get("Results", [])

    # set structure of the decoded object as empty strings
    decoded = {field: "" for field in _WANTED_FIELDS.values()}
    for item in results:
        key = _WANTED_FIELDS.get(item.get("Variable"))
        if key is not None:
            # set the value of the decoded object, ex: decoded["make"] = "BMW"
            decoded[key] = item.get("Value") or ""

    # if make/model are empty, throw error
    if not decoded["make"] and not decoded["model"]:
        raise VpicError(f"vPIC could not decode VIN {vin}")
    return decoded
