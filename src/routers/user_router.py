from fastapi import APIRouter, HTTPException, status, Depends
from src.services.user import UserService
from src.schemas.user import UserDTO, UserUpdateDTO
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_users(service: UserService = Depends(get_user_service)):
    users = service.get_all()
    return users
    

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):
    try:
        user = service.get_by_id(user_id)
        return user
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(data: UserDTO, service: UserService = Depends(get_user_service)):
    try:
        new_user = service.create(data=data)
        return new_user
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: UUID, data: UserUpdateDTO, service: UserService = Depends(get_user_service)):
    try:
        user = service.update(data=data)
        return user
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
            )
    
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    try:
        user = service.delete(user_id=user_id)
        return 
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )