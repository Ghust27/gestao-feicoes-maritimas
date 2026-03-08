from src.domain.interfaces.oil_feature_repository import IOilFeatureRepository
from src.schemas.oil_feature import OilFeatureDTO, OilFeatureUpdateDTO
from src.domain.entities.oil_feature import OilFeature
from uuid import UUID


class OilFeatureService:
    def __init__(self, oil_feature_repository: IOilFeatureRepository):
        self.oil_feature_repository = oil_feature_repository

    def get_all(self, status: str = None, min_confidence_level: int = None):
        oil_features = self.oil_feature_repository.get_all_oil_features(status,min_confidence_level)
        
        return oil_features
    
    def get_by_id(self, oil_feature_id: UUID):
        oil_feature = self.oil_feature_repository.get_oil_feature(oil_feature_id=oil_feature_id)
        return oil_feature
    
    def create(self, data: OilFeatureDTO) -> OilFeature:
        new_oil_feature = OilFeature(data=data)

        return self.oil_feature_repository.create_oil_feature(new_oil_feature)
    
    def update(self, oil_feature_id: str, data: OilFeatureUpdateDTO) -> OilFeature:
        oil_feature = self.oil_feature_repository.get_oil_feature(oil_feature_id)
        if not oil_feature:
            raise ValueError("Oil Feature not found.")
        if oil_feature.status in ["confirmed", "discarded"]:
            raise ValueError("It is not possible to change data for a confirmed or discarded feature.")
        
        return self.oil_feature_repository.update_oil_feature(id=oil_feature_id ,data=data)
    
    def delete(self, oil_feature_id: str) -> bool:
        oil_feature = self.oil_feature_repository.get_oil_feature(oil_feature_id)
        if not oil_feature:
            raise ValueError("oil_feature not found.")
        
        return self.oil_feature_repository.delete_vessel(oil_feature_id)