from fastapi import status, HTTPException, APIRouter, Depends, Request
from src.services.auth import AuthService
from src.api.dependencies import get_auth_service
from pydantic import BaseModel, EmailStr


class LoginDTO(BaseModel):
    email: EmailStr
    password: str

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login",status_code=status.HTTP_200_OK)
async def login(request: Request, service: AuthService = Depends(get_auth_service)):
    try:
        content_type = request.headers.get("content-type", "")

        if "application/json" in content_type:
            payload = await request.json()
            data = LoginDTO(**payload)
            email = data.email
            password = data.password
        else:
            form = await request.form()
            # OAuth2 Password flow sends username/password in form-encoded payload.
            username = form.get("username")
            password = form.get("password")
            if username is None or password is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Missing username/password in form data.",
                )
            data = LoginDTO(email=username, password=password)
            email = data.email
            password = data.password

        token_data = service.login(str(email), password)
        return token_data
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            headers={"WWW-Authenticate": "bearer"}
        )