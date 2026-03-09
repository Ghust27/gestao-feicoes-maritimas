from src.domain.interfaces.user_repository import IUserRepository
from src.schemas.user import UserDTO, UserUpdateDTO
from src.domain.entities.user import User
from uuid import UUID


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def create(self, data: UserDTO) -> User:
        user = self.user_repository.get_user_by_email(data.email)
        if user:
            raise ValueError("Email already registered.")
        new_user = User(data=data)

        return self.user_repository.create_user(new_user)
    
    def get_by_id(self, user_id):
        user = self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise ValueError("User not found.")
        return user


    def get_all(self):
        users = self.user_repository.get_all()
        if not users:
            raise ValueError("Users not found.")
        return users
    
    def update(self, user_id: UUID, data: UserUpdateDTO) -> User:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        
        return self.user_repository.update_user(id=user_id ,data=data)
    
    def delete(self, user_id: UUID) -> bool:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        confirmed_features_count = self.user_repository.confirmed_features_count(user_id)
        
        user.validate_delete(confirmed_features=confirmed_features_count)
        
        return self.user_repository.delete_user(user_id)