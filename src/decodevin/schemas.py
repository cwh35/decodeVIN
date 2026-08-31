from pydantic import BaseModel, Field, field_validator


class VinRequest(BaseModel):
    """Shared request body for /lookup and /remove."""

    vin: str = Field(..., min_length=17, max_length=17)

    @field_validator("vin")
    @classmethod
    def validate_vin(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("vin must be exactly 17 alphanumeric characters")
        return v.upper()


class LookupResponse(BaseModel):
    vin: str
    make: str
    model: str
    model_year: str
    body_class: str
    cached: bool


class RemoveResponse(BaseModel):
    vin: str
    cache_delete_success: bool
