from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class Status(str, Enum):
    DETECTED = "detected"
    CONFIRMED = "confirmed"
    DISCARDED = "discarded"

class OilFeatureDTO(BaseModel):
    latitude: float = Field(ge= -90.0, le= 90.0, description="Latitude should be between -90 and 90 degrees.")
    longitude: float = Field(ge= -180.0, le= 180.0, description="Longitude should be between -90 and 90 degrees.")
    estimated_area: float
    confidence_level: int = Field(ge= 0, le= 100, description="Confidence level should be between 0 and 100 degrees.")
    status: Status

class OilFeatureUpdateDTO(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    estimated_area: Optional[float] = None
    confidence_level: Optional[int] = None
    status: Optional[Status] = None

class VesselDTO(BaseModel):
    mmsi: str