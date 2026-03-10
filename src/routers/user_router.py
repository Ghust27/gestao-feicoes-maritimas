from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from src.api.dependencies import (
    get_user_service,
    require_admin,
    require_operator_or_admin,
)
from src.schemas.user import UserCreateDTO, UserUpdateDTO
from src.services.user import UserService


def _user_to_response(user):
    """Exclude hashed_password from API response."""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value if hasattr(user.role, "value") else user.role,
        "active": user.active,
        "created_at": user.created_at,
    }


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(
    service: UserService = Depends(get_user_service),
    current_user: dict = Depends(require_admin),
):
    users = service.get_all()
    return [_user_to_response(u) for u in users]


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user: dict = Depends(require_admin),
):
    try:
        user = service.get_by_id(user_id)
        return _user_to_response(user)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreateDTO, service: UserService = Depends(get_user_service)
):
    try:
        new_user = service.create(data=data)
        return _user_to_response(new_user)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(
    user_id: UUID,
    data: UserUpdateDTO,
    service: UserService = Depends(get_user_service),
    current_user: dict = Depends(require_operator_or_admin),
):
    try:
        user = service.update(user_id=user_id, data=data)
        return _user_to_response(user)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
            )
    
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service), current_user: dict = Depends(require_admin)):
    try:
        user = service.delete(user_id=user_id)
        return 
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )