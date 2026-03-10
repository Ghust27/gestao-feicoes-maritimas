# User: id (UUID), name, email (unique), password (hash), role (ADMIN, OPERATOR), active (bool),
# created_at. Full CRUD. Cannot delete if user has confirmed features.
from uuid import UUID, uuid4
from datetime import datetime, timezone
from src.schemas.user import UserDTO


class User:
    def __init__(
            self, data: UserDTO, 
            active: bool = True, created_at: datetime | None = None, 
            id: UUID | None = None
    ):
        self.id = id or uuid4()
        self.name = data.name
        self.email = data.email
        self.hashed_password = data.hashed_password
        self.role = data.role
        self.active = active
        self.created_at = created_at or datetime.now(timezone.utc)

    def validate_delete(self, confirmed_features: int):
        if confirmed_features > 0:
            raise ValueError("Cannot delete a user with confirmed features.")
        return True
    