from abc import ABC, abstractmethod
from src.domain.entities.vessel import Vessel
from src.schemas.vessel import VesselDTO, VesselUpdateDTO


class IVesselRepository(ABC):
    @abstractmethod
    def create_vessel(self, vessel: Vessel) -> Vessel:
        """Create a Vessel on the database and return the Vessel."""
        pass

    @abstractmethod
    def get_all(self) -> list:
        """Get all vessels from the database."""
        pass

    @abstractmethod
    def get_by_id(self, mmsi: str) -> Vessel | None:
        """Get the vessel information from the database using the mmsi."""
        pass

    @abstractmethod
    def get_associated_oil_features(self, vessel_mmsi: str) -> int:
        """Get the count of oil features associated with the vessel."""
        pass

    @abstractmethod
    def update_vessel(self, vessel_mmsi: str, data: VesselUpdateDTO) -> Vessel | None:
        """Update information about the vessel."""
        pass

    @abstractmethod
    def delete_vessel(self, vessel_mmsi: str) -> bool:
        """Delete the Vessel from database using the mmsi."""
        pass