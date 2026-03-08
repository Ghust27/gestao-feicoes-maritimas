from uuid import UUID, uuid4
from datetime import datetime, timezone

from src.schemas.oil_feature import OilFeatureDTO

class OilFeature:
    def __init__(
            self, data: OilFeatureDTO,
            id: UUID = None, detection_date: datetime = None, 
            confirmed_by: str = None, confirmation_date: datetime = None
    ):
        self.id = id or uuid4() 
        self.latitude = data.latitude 
        self.longitude = data.longitude 
        self.estimated_area = data.estimated_area 
        self.confidence_level = data.confidence_level 
        self.status = data.status 
        self.detection_date = detection_date or datetime.now(timezone.utc)
        self.confirmed_by = confirmed_by 
        self.confirmation_date = confirmation_date