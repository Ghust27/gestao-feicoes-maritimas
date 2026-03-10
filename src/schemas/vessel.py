import re
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class VesselTypes(str, Enum):
    OSV = "osv"
    AHTS = "ahts"
    RSV = "rsv"
    RV = "rv"
    PSV = "psv"
    PLSV = "plsv"


class VesselDTO(BaseModel):
    mmsi: str = Field(..., min_length=9, max_length=9, description="MMSI - 9 numeric digits")
    name: str
    vessel_type: VesselTypes
    imo: Optional[str] = None
    active: Optional[bool] = True

    @field_validator("mmsi")
    @classmethod
    def validate_mmsi(cls, v: str) -> str:
        if not re.match(r"^\d{9}$", v):
            raise ValueError("MMSI must be exactly 9 numeric digits")
        return v

class VesselUpdateDTO(BaseModel):
        name: Optional[str] = None
        vessel_type: Optional[VesselTypes] = None
        imo: Optional[str] = None
        active: Optional[bool] = True