from abc import ABC,abstractmethod
from src.domain.entities.vessel import Vessel
from uuid import UUID
from src.schemas.vessel import VesselDTO, VesselUpdateDTO


class IVesselRepository(ABC):
    @abstractmethod
    def create_vessel(self, Vessel: VesselDTO) -> Vessel:
        "Create a Vessel on the database and return the Vessel."
        pass

    @abstractmethod
    def get_all(self) -> list | None :
        """Get all Vessels informations from the database."""
        pass

    @abstractmethod
    def get_by_id(self, mmsi: str) -> Vessel | None :
        """Get the Vessel informations from the database using the id."""
        pass
        
    @abstractmethod
    def get_vessel_status(self, mmsi: str) -> str:
        """Get the Vessel status using the id."""
        pass

    @abstractmethod
    def get_associated_oil_features(self, vessel_mmsi: str)-> int:
        """"Get the Vessel associated oil features."""
        pass

    @abstractmethod
    def update_vessel(self, vessel_mmsi: str, data: VesselUpdateDTO) -> Vessel | None:
        """Update informations about the vessel."""
        pass

    @abstractmethod
    def delete_vessel(self, vessel_mmsi: str) -> bool:
        """Delete the Vessel from database using the id."""
        pass

    @abstractmethod
    def confirm_oil_feature(self, oil_feature_id: str) -> bool:
        """Confirm a oil feature"""
        pass