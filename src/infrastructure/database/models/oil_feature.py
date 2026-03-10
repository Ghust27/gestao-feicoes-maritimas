import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Table, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.infrastructure.database.models.vessel import VesselModel

oil_feature_vessels = Table(
    "oil_feature_vessels",
    Base.metadata,
    Column("oil_feature_id", UUID(as_uuid=True), ForeignKey("oil_features.id"), primary_key=True),
    Column("vessel_mmsi", String(9), ForeignKey("vessels.mmsi"), primary_key=True)
)

class OilFeatureModel(Base):
    __tablename__ = "oil_features"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    estimated_area = Column(Float, nullable=False)
    confidence_level = Column(Integer, nullable=False)
    status = Column(String, default="DETECTED", nullable=False) 
    detection_date = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    confirmed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    confirmation_date = Column(DateTime, nullable=True)

    vessels = relationship("VesselModel", secondary=oil_feature_vessels, backref="oil_features")
    
    __table_args__ = (
        CheckConstraint('latitude >= -90 AND latitude <= 90', name='check_latitude'),
        CheckConstraint('longitude >= -180 AND longitude <= 180', name='check_longitude'),
        CheckConstraint('confidence_level >= 0 AND confidence_level <= 100', name='check_confidence_level'),
    )