from src.domain.interfaces.vessel_repository import IVesselRepository
from src.schemas.vessel import VesselDTO, VesselUpdateDTO
from src.domain.entities.vessel import Vessel
from uuid import UUID


class VesselService:
    def __init__(self, vessel_repository: IVesselRepository):
        self.vessel_repository = vessel_repository
    
    def create(self, data: VesselDTO) -> Vessel:
        vessel = self.vessel_repository.get_by_id(data.mmsi)
        if vessel:
            raise ValueError("Vessel already registered.")
        new_vessel = Vessel(data=data)

        return self.vessel_repository.create_vessel(new_vessel)
    
    def get_by_id(self, mmsi: str) -> Vessel:
        vessel = self.vessel_repository.get_by_id(mmsi=mmsi)
        if not vessel:
            raise ValueError("Vessel not found.")
        return vessel
    
    def get_all(self, mmsi: str) -> Vessel:
        vessels = self.vessel_repository.get_all()
        if not vessels:
            raise ValueError("Vessels not found.")
        return vessels
    
    def update(self, mmsi: str, data: VesselUpdateDTO) -> Vessel:
        vessel = self.vessel_repository.get_by_id(mmsi)
        if not vessel:
            raise ValueError("Vessel not found.")
        
        return self.vessel_repository.update_vessel(id=mmsi ,data=data)
    
    def delete(self, mmsi: str) -> bool:
        vessel = self.vessel_repository.get_by_id(mmsi)
        if not vessel:
            raise ValueError("Vessel not found.")
        associated_oil_features = self.vessel_repository.get_associated_oil_features(mmsi)
        
        vessel.validate_delete(associated_features=associated_oil_features)
        
        return self.vessel_repository.delete_vessel(mmsi)
    