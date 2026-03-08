from src.domain.interfaces.oil_feature_repository import IOilFeatureRepository
from src.domain.interfaces.user_repository import IUserRepository
from uuid import UUID

class DiscardOilFeatureService:
    def __init__(self,oil_feature_repository: IOilFeatureRepository, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.oil_feature_repository = oil_feature_repository

    def execute(self, user_id: UUID, oil_feature_id: UUID):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Invalid User.")
        if user.role != "admin":
            raise ValueError("Only admin users can discard oil features.")
        
        oil_feature = self.oil_feature_repository.get_oil_feature(oil_feature_id)
        if not oil_feature:
            raise ValueError("Oil feature not found.")

        return self.user_repository.discard_oil_feature(oil_feature_id)