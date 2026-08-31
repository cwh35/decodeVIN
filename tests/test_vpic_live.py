"""
Tests in this file make real network calls to the vPIC API (no mocking).
Run only these with:  uv run pytest -m network
Skip them with:       uv run pytest -m "not network"
"""

import logging

import pytest

logger = logging.getLogger(__name__)

# Test VINs listed in INSTRUCTIONS.md
INSTRUCTIONS_TEST_VINS = [
    "1HGCM82633A004352",
    "5YJ3E1EA6PF384836",
    "1FTFW1ET9DFC10312",
    "1C4RJFBG2FC625797",
    "5FNRL6H79NB021411",
    "1HD1KBM15FB620271",
    "1XPWD40X1ED215307",
]


@pytest.mark.network
@pytest.mark.parametrize("vin", INSTRUCTIONS_TEST_VINS)
def test_lookup_decodes_each_instructions_test_vin(client, vin):
    response = client.post("/lookup", json={"vin": vin})

    assert response.status_code == 200
    body = response.json()
    assert body["vin"] == vin
    assert body["make"], f"expected a non-empty make for {vin}"
    assert body["model"], f"expected a non-empty model for {vin}"
    assert body["cached"] is False


@pytest.mark.network
def test_lookup_decodes_custom_vin(client, custom_vin):
    """
    Pass any VIN you want to test with --vin, e.g.:

        uv run pytest tests/test_vpic_live.py -m network --vin=1HGCM82633A004352
    """
    if not custom_vin:
        pytest.skip(
            "no --vin given; pass one to test a specific VIN, e.g. "
            "pytest tests/test_vpic_live.py -m network --vin=1HGCM82633A004352"
        )

    response = client.post("/lookup", json={"vin": custom_vin})

    if response.status_code != 200:
        logger.error(
            "Lookup failed for VIN %r -- status=%s detail=%s",
            custom_vin,
            response.status_code,
            response.json(),
        )
        pytest.fail(
            f"Lookup failed for VIN {custom_vin!r}: "
            f"status={response.status_code} detail={response.json()}"
        )

    body = response.json()
    logger.info(
        "Lookup succeeded for VIN %s -- make=%s model=%s model_year=%s body_class=%s cached=%s",
        body["vin"],
        body["make"],
        body["model"],
        body["model_year"],
        body["body_class"],
        body["cached"],
    )

    assert body["vin"] == custom_vin.upper()
