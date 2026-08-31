"""
pydantic is FastAPI's data-validation layer
BaseModel = base class every request/response inherits from
Field = attach constraints to individual fields
field_validator = custom validation logic beyond Field's constraints
"""

from pydantic import BaseModel, Field, field_validator


class VinRequest(BaseModel):
    """shared request body for /lookup and /remove."""

    # ... = this field is required, if vin is missing, it will error out
    vin: str = Field(..., min_length=17, max_length=17)

    @field_validator("vin") 
    @classmethod
    def validate_vin(cls, v: str) -> str:
        if not v.isalnum():
            # check if every character is a letter or digit
            raise ValueError("vin must be exactly 17 alphanumeric characters")
        return v.upper() # make sure the VIN is converted to uppercase


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

""" 
/export doesn't need an object because it doesn't take any inputs 
and it outputs a binary file and not a structured response object
"""
