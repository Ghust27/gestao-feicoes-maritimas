from abc import ABC, abstractmethod
from src.domain.entities.oil_feature import OilFeature
from uuid import UUID
from src.schemas.oil_feature import OilFeatureDTO, OilFeatureUpdateDTO


class IOilFeatureRepository(ABC):
    @abstractmethod
    def get_oil_feature(self, oil_feature_id: UUID) -> OilFeature | None:
        """Get the oil feature information from the database using the id."""
        pass

    @abstractmethod
    def get_all_oil_features(
        self, status: str = None, min_confidence_level: int = None
    ) -> list:
        """Get all oil features, may or may not contain filters."""
        pass

    @abstractmethod
    def create_oil_feature(self, oil_feature: OilFeature) -> OilFeature:
        """Create an oil feature on the database and return the OilFeature."""
        pass

    @abstractmethod
    def update_oil_feature(
        self, oil_feature_id: UUID, data: OilFeatureUpdateDTO
    ) -> OilFeature | None:
        """Update information about the oil feature."""
        pass

    @abstractmethod
    def delete_oil_feature(self, oil_feature_id: UUID) -> bool:
        """Delete the oil feature from database using the id."""
        pass

    @abstractmethod
    def associate_oil_feature_with_vessel(
        self, oil_feature_id: UUID, vessel_mmsi: str
    ) -> bool:
        """Associate the oil feature to a vessel."""
        pass

    @abstractmethod
    def disassociate_oil_feature_with_vessel(
        self, oil_feature_id: UUID, vessel_mmsi: str
    ) -> bool:
        """Disassociate the oil feature from a vessel."""
        pass

    @abstractmethod
    def confirm_oil_feature(self, oil_feature_id: UUID, user_id: UUID) -> OilFeature | None:
        """Confirm an oil feature (set status CONFIRMED, confirmed_by, confirmation_date)."""
        pass

    @abstractmethod
    def discard_oil_feature(self, oil_feature_id: UUID) -> OilFeature | None:
        """Discard an oil feature (set status DISCARDED)."""
        pass
    