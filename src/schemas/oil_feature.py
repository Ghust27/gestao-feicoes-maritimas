from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class Status(str, Enum):
    DETECTED = "DETECTED"
    CONFIRMED = "CONFIRMED"
    DISCARDED = "DISCARDED"


class OilFeatureDTO(BaseModel):
    latitude: float = Field(ge=-90.0, le=90.0, description="Latitude between -90 and 90 degrees.")
    longitude: float = Field(ge=-180.0, le=180.0, description="Longitude between -180 and 180 degrees.")
    estimated_area: float
    confidence_level: int = Field(ge=0, le=100, description="Confidence level between 0 and 100.")
    status: Optional[Status] = Status.DETECTED

class OilFeatureUpdateDTO(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    estimated_area: Optional[float] = None
    confidence_level: Optional[int] = None
    status: Optional[Status] = None

class VesselDTO(BaseModel):
    mmsi: str