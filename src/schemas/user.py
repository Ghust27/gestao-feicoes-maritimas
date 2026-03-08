from pydantic import BaseModel
from enum import Enum
from typing import Optional
from uuid import UUID

class Role(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"

class UserDTO(BaseModel):
    name: str
    email: str
    hashed_password: str
    role: Role

class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    role: Optional[Role] = None