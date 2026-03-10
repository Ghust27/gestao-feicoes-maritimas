from uuid import UUID
from src.domain.interfaces.user_repository import IUserRepository
from src.domain.interfaces.oil_feature_repository import IOilFeatureRepository


class ConfirmOilFeatureService:
    def __init__(
        self,
        user_repository: IUserRepository,
        oil_feature_repository: IOilFeatureRepository,
    ):
        self.user_repository = user_repository
        self.oil_feature_repository = oil_feature_repository

    def execute(self, user_id: UUID, oil_feature_id: UUID):
        """Only active users can confirm oil features."""
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Invalid user.")
        if not self.user_repository.is_user_active(user_id):
            raise ValueError("Only active users can confirm oil features.")

        oil_feature = self.oil_feature_repository.get_oil_feature(oil_feature_id)
        if not oil_feature:
            raise ValueError("Oil feature not found.")

        status_val = oil_feature.status.value if hasattr(oil_feature.status, "value") else str(oil_feature.status)
        if status_val == "CONFIRMED":
            raise ValueError("Oil feature is already confirmed.")
        if status_val == "DISCARDED":
            raise ValueError("Cannot confirm a discarded oil feature.")

        return self.oil_feature_repository.confirm_oil_feature(oil_feature_id, user_id)