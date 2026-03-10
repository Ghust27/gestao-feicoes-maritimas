from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"


class UserCreateDTO(BaseModel):
    """Schema for creating a user - password is hashed by the service."""
    name: str
    email: EmailStr
    password: str
    role: Role = Role.OPERATOR


class UserDTO(BaseModel):
    name: str
    email: str
    hashed_password: str
    role: Role


class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Role] = None


class UserResponseDTO(BaseModel):
    """Response schema - excludes password."""

    id: UUID
    name: str
    email: str
    role: Role
    active: bool
    created_at: datetime

    model_config = {"from_attributes": True}