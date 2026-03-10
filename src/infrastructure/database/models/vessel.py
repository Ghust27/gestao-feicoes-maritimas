from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime
from src.core.database import Base

class VesselModel(Base):
    __tablename__ = "vessels"

    mmsi = Column(String(9), primary_key=True, index=True) 
    name = Column(String, nullable=False)
    imo = Column(String, unique=True, nullable=True) 
    vessel_type = Column(String, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)