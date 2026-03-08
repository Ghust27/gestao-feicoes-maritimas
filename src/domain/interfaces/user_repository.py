from abc import ABC,abstractmethod
from src.domain.entities.user import User
from uuid import UUID
from src.schemas.user import UserUpdateDTO, UserDTO


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserDTO) -> User:
        "Create a user on the database and return the user."
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> User | None :
        """Get the user informations from the database using the id."""
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        """Get the user informations from the database using the email."""
        pass
    
    @abstractmethod
    def validate_user_status(self, user_id) -> bool:
        """Get the user status using the id."""
        pass
    
    @abstractmethod
    def get_user_role(self, user_id) -> str:
        """Get the user role using the id."""
        pass
    
    @abstractmethod
    def update_user(self,user_id: UUID, data: UserUpdateDTO) -> User | None:
        """Update informations about the user."""
        pass

    @abstractmethod
    def delete_user(self, user_id: UUID) -> bool:
        """Delete the user from database using the id."""
        pass

    @abstractmethod
    def confirmed_features_count(self, user_id: UUID) -> int:
        """Search for user associations with oil features."""
        pass

    @abstractmethod
    def discard_oil_feature(self, oil_feature_id: UUID) -> bool:
        """Discard oil feature."""
        pass