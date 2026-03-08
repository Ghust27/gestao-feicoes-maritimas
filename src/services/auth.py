from src.core.security import verify_password, create_acess_token
from src.domain.interfaces.user_repository import IUserRepository

class AuthService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository 

    def login(self, email: str, password: str) -> str:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("Incorrect email or password.")
        
        if not verify_password(password,user.hashed_password):
            raise ValueError("Incorrect email or password.")
        
        token_data = {"sub": str(user.id)}
        token = create_acess_token(data=token)

        return {
            "access_token": token,
            "token_type": "bearer"
        }