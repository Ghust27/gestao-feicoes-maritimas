from abc import ABC, abstractmethod
from src.domain.entities.user import User
from uuid import UUID
from src.schemas.user import UserDTO


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        """Create a user on the database and return the user."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> User | None:
        """Get the user information from the database using the id."""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        """Get the user information from the database using the email."""
        pass

    @abstractmethod
    def get_all(self) -> list:
        """Get all users from the database."""
        pass

    @abstractmethod
    def is_user_active(self, user_id: UUID) -> bool:
        """Check if the user is active."""
        pass

    @abstractmethod
    def update_user(self, user_id: UUID, data: dict) -> User | None:
        """Update information about the user."""
        pass

    @abstractmethod
    def delete_user(self, user_id: UUID) -> bool:
        """Delete the user from database using the id."""
        pass

    @abstractmethod
    def confirmed_features_count(self, user_id: UUID) -> int:
        """Count oil features confirmed by this user."""
        pass