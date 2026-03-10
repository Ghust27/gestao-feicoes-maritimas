from uuid import UUID

from src.core.security import get_password_hash
from src.domain.entities.user import User
from src.domain.interfaces.user_repository import IUserRepository
from src.schemas.user import UserCreateDTO, UserDTO, UserUpdateDTO


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def create(self, data: UserCreateDTO) -> User:
        user = self.user_repository.get_user_by_email(data.email)
        if user:
            raise ValueError("Email already registered.")
        user_dto = UserDTO(
            name=data.name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            role=data.role,
        )
        new_user = User(data=user_dto)
        return self.user_repository.create_user(new_user)
    
    def get_by_id(self, user_id):
        user = self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise ValueError("User not found.")
        return user


    def get_all(self):
        return self.user_repository.get_all()
    
    def update(self, user_id: UUID, data: UserUpdateDTO) -> User:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        return self.user_repository.update_user(user_id=user_id, data=update_data)
    
    def delete(self, user_id: UUID) -> bool:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        confirmed_features_count = self.user_repository.confirmed_features_count(user_id)
        
        user.validate_delete(confirmed_features=confirmed_features_count)
        
        return self.user_repository.delete_user(user_id)