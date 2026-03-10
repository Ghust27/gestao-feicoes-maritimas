from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
import os
from dotenv import load_dotenv

from src.core.database import get_db
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.vessel import VesselRepository
from src.infrastructure.repositories.oil_feature import OilFeatureRepository
from src.services.auth import AuthService
from src.services.user import UserService
from src.services.vessel import VesselService
from src.services.oil_feature import OilFeatureService
from src.services.associate_oil_feature import AssociateOilFeatureService
from src.services.confirm_oil_feature import ConfirmOilFeatureService
from src.services.discard_oil_feature import DiscardOilFeatureService

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM", "HS256")
SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_vessel_repository(db: Session = Depends(get_db)) -> VesselRepository:
    return VesselRepository(db)


def get_oil_feature_repository(db: Session = Depends(get_db)) -> OilFeatureRepository:
    return OilFeatureRepository(db)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repo)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=user_repo)


def get_vessel_service(
    vessel_repo: VesselRepository = Depends(get_vessel_repository),
) -> VesselService:
    return VesselService(vessel_repository=vessel_repo)


def get_oil_feature_service(
    oil_feature_repo: OilFeatureRepository = Depends(get_oil_feature_repository),
) -> OilFeatureService:
    return OilFeatureService(oil_feature_repository=oil_feature_repo)


def get_associate_oil_feature_service(
    oil_feature_repo: OilFeatureRepository = Depends(get_oil_feature_repository),
    vessel_repo: VesselRepository = Depends(get_vessel_repository),
) -> AssociateOilFeatureService:
    return AssociateOilFeatureService(
        oil_feature_repository=oil_feature_repo,
        vessel_repository=vessel_repo,
    )


def get_confirm_oil_feature_service(
    user_repo: UserRepository = Depends(get_user_repository),
    oil_feature_repo: OilFeatureRepository = Depends(get_oil_feature_repository),
) -> ConfirmOilFeatureService:
    return ConfirmOilFeatureService(
        user_repository=user_repo,
        oil_feature_repository=oil_feature_repo,
    )


def get_discard_oil_feature_service(
    oil_feature_repo: OilFeatureRepository = Depends(get_oil_feature_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> DiscardOilFeatureService:
    return DiscardOilFeatureService(
        oil_feature_repository=oil_feature_repo,
        user_repository=user_repo,
    )

def get_current_user_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or incomplete token."
            )
        return {"id": user_id, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your session has expired (Token expired)."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )

def require_admin(current_user: dict = Depends(get_current_user_token)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )
    return current_user

def require_operator_or_admin(current_user: dict = Depends(get_current_user_token)):
    if current_user["role"] not in ["admin", "operator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access denied.")
    return current_user