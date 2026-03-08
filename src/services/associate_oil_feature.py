from src.domain.interfaces.oil_feature_repository import IOilFeatureRepository
from src.domain.interfaces.vessel_repository import IVesselRepository
from uuid import UUID

class AssociateOilFeatureService:
    def __init__(self, oil_feature_repository: IOilFeatureRepository, vessel_repository: IVesselRepository):
        self.oil_feature_repository = oil_feature_repository
        self.vessel_repository = vessel_repository

    def associate(self, mmsi: str, oil_feature_id: UUID)->bool:
        oil_feature = self.oil_feature_repository.get_oil_feature(oil_feature_id)
        if not oil_feature:
            raise ValueError("Oil feature not found.")
        vessel = self.vessel_repository.get_vessel(mmsi)
        if not vessel:
            raise ValueError("Vessel not found.")
        if not vessel.active:
            raise ValueError("Cannot associate oil feature with inactive vessel.")
        return self.oil_feature_repository.associate_oil_feature_with_vessel(oil_feature_id=oil_feature_id,vessel_mmsi=mmsi)
    
    def disassociate(self, mmsi: str, oil_feature_id: UUID)->bool:
        oil_feature = self.oil_feature_repository.get_oil_feature(oil_feature_id)
        if not oil_feature:
            raise ValueError("Oil feature not found.")
        vessel = self.vessel_repository.get_vessel(mmsi)
        if not vessel:
            raise ValueError("Vessel not found.")

        return self.oil_feature_repository.disassociate_oil_feature_with_vessel(oil_feature_id=oil_feature_id,vessel_mmsi=mmsi)