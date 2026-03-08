from fastapi import status, HTTPException, APIRouter, Depends
from src.services.auth import AuthService
from pydantic import BaseModel, EmailStr


class LoginDTO(BaseModel):
    email: EmailStr
    password: str

router = APIRouter("/auth", tags=["Authentication"])

@router.post("/login",status_code=status.HTTP_200_OK)
def login(data: LoginDTO, service: AuthService = Depends(get_auth_service)):
    try:
        token_data = service.login(data.email, data.password)
        return token_data
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            headers={"WWW-Authenticate": "bearer"}
        )