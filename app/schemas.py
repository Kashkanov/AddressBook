from typing import Optional
from pydantic import BaseModel, Field, field_validator


class AddressCreate(BaseModel):
    
    label: Optional[str] = Field(None, max_length=100, examples=["Home"])
    houseNo: str = Field(...,  min_length=1, max_length=255)
    street: str = Field(...,  min_length=1, max_length=255)
    barangay: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=100)
    region: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    
    @field_validator("houseNo", "street", "city", "country")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()
    
class AddressUpdate(BaseModel):
    label: Optional[str] = Field(None)
    houseNo: Optional[str] = Field(None, min_length=1)
    street: Optional[str] = Field(None, min_length=1)
    barangay: Optional[str] = Field(None, min_length=1)
    city: Optional[str] = Field(None, min_length=1)
    region: Optional[str] = Field(None, min_length=1)
    country: Optional[str] = Field(None, min_length=1)
    latitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    
class AddressResponse(BaseModel):
    id: int
    label: Optional[str]
    houseNo: str
    street: str
    barangay: str
    city: str
    region: str
    country: str
    latitude: float
    longitude: float
    model_config = {"from_attributes": True}
    