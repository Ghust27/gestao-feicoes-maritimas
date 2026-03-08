from uuid import UUID
from src.domain.interfaces.vessel_repository import IVesselRepository
from src.domain.interfaces.oil_feature_repository import IOilFeatureRepository

class ConfirmOilFeatureService:
    def __init__(self, vessel_repository: IVesselRepository, oil_feature_repository: IOilFeatureRepository):
        self.vessel_repository = vessel_repository
        self.oil_feature_repository = oil_feature_repository

    def execute(self, mmsi: str, oil_feature_id: UUID):
        vessel = self.vessel_repository.get_vessel(mmsi)
        if not vessel:
            raise ValueError("Only vessels can confirm oil features.")
        
        if not vessel.active:
            raise ValueError("Only active vessels can confirm oil features.")

        oil_feature = self.oil_feature_repository.get_oil_feature(oil_feature_id)
        if not oil_feature:
            raise ValueError("Oil feature not found.")
        return self.vessel_repository.confirm_oil_feature(oil_feature_id)