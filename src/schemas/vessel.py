from enum import Enum
from pydantic import BaseModel
from typing import Optional


class VesselTypes(str, Enum):
        OSV = "osv"
        AHTS = "ahts"
        RSV = "rsv"
        RV = "rv"
        PSV = "psv"
        PLSV = "plsv"


class VesselDTO(BaseModel):
        mmsi: str 
        name: str 
        vessel_type: VesselTypes
        imo: Optional[str] = None
        active: Optional[bool] = True

class VesselUpdateDTO(BaseModel):
        name: Optional[str] = None
        vessel_type: Optional[VesselTypes] = None
        imo: Optional[str] = None
        active: Optional[bool] = True